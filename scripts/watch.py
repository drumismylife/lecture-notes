#!/usr/bin/env python3
from __future__ import annotations
"""
watch.py — 전용 입력 폴더 감시: HTML 저장되면 자동 배치 + 배포

감시 폴더: ~/Desktop/대학원/lecture-notes/input/
  → 처리 완료 후: input/done/ 으로 이동

사용법:
  python3 scripts/watch.py        # 감시 시작 (Ctrl+C로 종료)
"""

import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
ROOT_DIR = SCRIPTS_DIR.parent

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("❌ watchdog 미설치. 먼저 실행하세요: python3 scripts/setup.py")
    sys.exit(1)


# ── 설정 로드 ──────────────────────────────────────────────────────────────

def load_config() -> dict:
    config_path = SCRIPTS_DIR / "config.json"
    if not config_path.exists():
        print("❌ config.json 없음. python3 scripts/setup.py 를 먼저 실행하세요.")
        sys.exit(1)
    return json.loads(config_path.read_text(encoding="utf-8"))


# ── macOS 다이얼로그 ────────────────────────────────────────────────────────

def _osascript(script: str) -> str:
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def ask_subject_dialog(subjects: list) -> str:
    items = '", "'.join(subjects)
    script = (
        f'set choices to {{"{items}"}}\n'
        f'choose from list choices '
        f'with prompt "어느 과목의 노트인가요?" '
        f'with title "강의노트 자동화" '
        f'OK button name "선택" cancel button name "건너뛰기"'
    )
    result = _osascript(script)
    return None if result == "false" else result.strip()


def ask_week_dialog(suggested: int) -> str:
    script = (
        f'display dialog '
        f'"몇 주차인가요?\\n추가자료면 숫자+b (예: {suggested}b)\\n\\n현재 최신: {suggested - 1}주차" '
        f'with title "강의노트 자동화" '
        f'default answer "{suggested}" '
        f'buttons {{"취소", "확인"}} default button "확인"'
    )
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    m = re.search(r"text returned:(.+)", result.stdout)
    return m.group(1).strip() if m else None


def notify(title: str, message: str) -> None:
    script = f'display notification "{message}" with title "{title}" sound name "Glass"'
    _osascript(script)


# ── 주차 유틸 ──────────────────────────────────────────────────────────────

def parse_week(week_str: str) -> tuple:
    """'10' → (10, '')  /  '10b' → (10, 'b')"""
    m = re.match(r"^0*(\d+)([a-z]?)$", week_str.strip().lower())
    if not m:
        return None, ""
    return int(m.group(1)), m.group(2)


def latest_week_in_output(output_dir: Path) -> int:
    """output 폴더에서 가장 큰 주차 번호 반환 (없으면 0)"""
    if not output_dir.exists():
        return 0
    max_w = 0
    for f in output_dir.iterdir():
        m = re.match(r"week(\d+)", f.name)
        if m:
            max_w = max(max_w, int(m.group(1)))
    return max_w


# ── 핵심 처리 ──────────────────────────────────────────────────────────────

def process_note(html_path: Path, config: dict, done_dir: Path) -> None:
    subjects_cfg = config["subjects"]
    semesters_cfg = config["semesters"]
    paths_cfg = config["paths"]
    subject_list = list(subjects_cfg.keys())

    ln_root = Path(paths_cfg["lecture_notes_root"]).expanduser()

    print(f"\n  ┌─ 새 파일: {html_path.name}")

    # 1) 과목 선택
    subject = ask_subject_dialog(subject_list)
    if not subject:
        print("  └─ 건너뜀 (input/done/ 으로 이동)")
        shutil.move(str(html_path), str(done_dir / html_path.name))
        return
    print(f"  │  과목: {subject}")

    subj_cfg = subjects_cfg[subject]
    sem_id = subj_cfg["semester"]
    # 과목이 속한 학기의 semester_base를 config.json에서 동적으로 조회 (전역 기본값에 고정하지 않음)
    semester_base = Path(semesters_cfg[sem_id]["semester_base"]).expanduser()
    semester_folder = subj_cfg["semester_folder"]
    output_folder = subj_cfg["output_folder"]
    output_dir = ln_root / "output" / output_folder

    # 2) 주차 선택 (다음 주차 자동 제안)
    latest = latest_week_in_output(output_dir)
    suggested = latest + 1
    week_str = ask_week_dialog(suggested)

    if not week_str:
        print("  └─ 취소됨")
        return

    week_num, variant = parse_week(week_str)
    if week_num is None:
        notify("⚠️ 형식 오류", f"'{week_str}' 은 올바른 주차 형식이 아닙니다.")
        print(f"  └─ 주차 형식 오류: {week_str}")
        return

    label = f"week{week_num:02d}{variant}"
    print(f"  │  주차: {label}")

    # 3) 1학기/[과목]/노트/ 에 원본 이름으로 저장
    notes_dir = semester_base / semester_folder / "노트"
    notes_dir.mkdir(parents=True, exist_ok=True)
    dst_note = notes_dir / html_path.name
    shutil.copy2(html_path, dst_note)
    print(f"  │  ✅ 노트/ → {html_path.name}")

    # 4) output/[폴더]/weekNN[b].html 로 저장
    output_dir.mkdir(parents=True, exist_ok=True)
    dst_output = output_dir / f"{label}.html"
    shutil.copy2(html_path, dst_output)
    print(f"  │  ✅ output/{output_folder}/{label}.html")

    # 5) deploy.py 실행
    print(f"  │  🚀 배포 중...")
    deploy_result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "deploy.py"), subject, label, "--semester", sem_id],
        capture_output=True, text=True,
        cwd=str(ln_root)
    )

    if deploy_result.returncode == 0:
        for line in deploy_result.stdout.strip().splitlines():
            print(f"  │    {line}")
        print(f"  └─ ✅ 배포 완료!")
        notify("✅ 노트 배포 완료",
               f"{subject} {week_num}주차{' (' + variant + ')' if variant else ''} — GitHub Pages 업로드됨")
    else:
        print(f"  └─ ❌ 배포 실패")
        print(deploy_result.stdout)
        print(deploy_result.stderr)
        notify("❌ 배포 실패", f"{subject} {week_num}주차 — 터미널을 확인하세요")

    # 6) 처리 완료 → done/ 으로 이동
    done_dir.mkdir(exist_ok=True)
    shutil.move(str(html_path), str(done_dir / html_path.name))
    print(f"     📁 원본 → input/done/{html_path.name}")


# ── watchdog 이벤트 핸들러 ─────────────────────────────────────────────────

class NoteHandler(FileSystemEventHandler):
    def __init__(self, config: dict, done_dir: Path):
        self.config = config
        self.done_dir = done_dir
        self._seen: set = set()

    def _should_process(self, path: Path) -> bool:
        if path.suffix.lower() != ".html":
            return False
        if path in self._seen:
            return False
        if path.name.startswith("."):
            return False
        # done/ 폴더 내 파일은 무시
        if path.parent == self.done_dir:
            return False
        # 파일이 완전히 쓰여질 때까지 대기
        time.sleep(1)
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            return False
        if size < 3000:
            return False
        return True

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if not self._should_process(path):
            return
        self._seen.add(path)
        process_note(path, self.config, self.done_dir)

    def on_moved(self, event):
        if event.is_directory:
            return
        path = Path(event.dest_path)
        if not self._should_process(path):
            return
        self._seen.add(path)
        process_note(path, self.config, self.done_dir)


# ── 메인 ──────────────────────────────────────────────────────────────────

def main():
    config = load_config()
    paths = config["paths"]

    watch_folder = Path(paths.get("watch_folder", paths["lecture_notes_root"] + "/input")).expanduser()
    done_dir = watch_folder / "done"

    watch_folder.mkdir(parents=True, exist_ok=True)
    done_dir.mkdir(exist_ok=True)

    print("=" * 52)
    print("  👁  강의노트 자동화 감시 시작")
    print("=" * 52)
    print(f"  감시 폴더: {watch_folder}")
    print()
    print("  Claude.ai에서 노트 완성 후 HTML을 아래 폴더에 저장하세요:")
    print(f"  👉 {watch_folder}")
    print()
    print("  Ctrl+C 로 종료\n")

    handler = NoteHandler(config, done_dir)
    observer = Observer()
    observer.schedule(handler, str(watch_folder), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n종료 중...")
        observer.stop()

    observer.join()
    print("감시 종료.")


if __name__ == "__main__":
    main()
