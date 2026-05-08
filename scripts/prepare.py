#!/usr/bin/env python3
from __future__ import annotations
"""
prepare.py — 수업 후 실행: 녹취 파일 준비 + Claude.ai 프로젝트 열기

사용법:
  python3 scripts/prepare.py                  # Downloads에서 자동 감지
  python3 scripts/prepare.py [녹취파일경로]   # 직접 지정
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPTS_DIR / "config.json"


def load_config():
    if not CONFIG_PATH.exists():
        print("❌ config.json이 없습니다. 먼저 setup.py를 실행하세요.")
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def find_recent_txt(downloads: Path, hours: int = 6) -> list:
    """Downloads에서 최근 N시간 내 .txt 파일 목록 (최신순)"""
    cutoff = (datetime.now() - timedelta(hours=hours)).timestamp()
    files = [
        f for f in downloads.iterdir()
        if f.suffix.lower() == ".txt"
        and not f.name.startswith(".")
        and f.stat().st_mtime > cutoff
    ]
    return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)


def detect_subject(txt_path: Path, subjects: dict) -> str | None:
    """파일명 + 내용 앞부분으로 과목 자동 추론"""
    name_lower = txt_path.stem.lower()

    # 1차: 파일명에서 키워드 탐색
    for subj, conf in subjects.items():
        for kw in conf["keywords"]:
            if kw.lower() in name_lower:
                return subj

    # 2차: 내용 첫 500자에서 키워드 탐색
    try:
        content = txt_path.read_text(encoding="utf-8", errors="ignore")[:500].lower()
        for subj, conf in subjects.items():
            for kw in conf["keywords"]:
                if kw.lower() in content:
                    return subj
    except Exception:
        pass

    return None


def pick_txt_file(downloads: Path) -> Path | None:
    """Downloads에서 녹취 파일 선택"""
    recent = find_recent_txt(downloads)

    if not recent:
        print("⚠️  Downloads에서 최근 6시간 내 .txt 파일이 없습니다.")
        path_input = input("파일 경로를 직접 입력하세요 (Enter=건너뜀): ").strip()
        if path_input:
            p = Path(path_input).expanduser()
            return p if p.exists() else None
        return None

    if len(recent) == 1:
        mtime = datetime.fromtimestamp(recent[0].stat().st_mtime).strftime("%H:%M")
        print(f"📄 녹취 파일 감지: {recent[0].name}  ({mtime})")
        return recent[0]

    print("📄 최근 녹취 파일 목록:")
    for i, f in enumerate(recent, 1):
        mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%H:%M")
        print(f"  [{i}] {f.name}  ({mtime})")
    raw = input("선택 (번호): ").strip()
    try:
        return recent[int(raw) - 1]
    except (ValueError, IndexError):
        return None


def pick_subject(subjects: dict, detected: str | None) -> str | None:
    """과목 선택 (감지된 과목 우선 제안)"""
    subject_list = list(subjects.keys())

    if detected:
        print(f"\n📚 감지된 과목: {detected}")
        confirm = input("맞나요? (Enter=예 / 번호로 변경): ").strip()
        if confirm == "":
            return detected
        try:
            return subject_list[int(confirm) - 1]
        except (ValueError, IndexError):
            return detected

    print("\n📚 과목 선택:")
    for i, s in enumerate(subject_list, 1):
        print(f"  [{i}] {s}")
    raw = input("번호: ").strip()
    try:
        return subject_list[int(raw) - 1]
    except (ValueError, IndexError):
        return None


def show_materials(materials_dir: Path) -> None:
    """강의자료 폴더의 최근 파일 목록 출력"""
    if not materials_dir.exists():
        print("  (강의자료 폴더 없음)")
        return
    files = sorted(
        [f for f in materials_dir.iterdir() if not f.name.startswith(".")],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not files:
        print("  (파일 없음)")
        return
    for i, f in enumerate(files[:10], 1):
        mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%m/%d")
        print(f"  {i:2}. [{mtime}] {f.name}")


def main():
    config = load_config()
    subjects = config["subjects"]
    paths = config["paths"]

    downloads = Path(paths["downloads"]).expanduser()
    semester_base = Path(paths["semester_base"]).expanduser()

    print("=" * 50)
    print("  📋 강의노트 업로드 준비")
    print("=" * 50)

    # 1) 녹취 파일 직접 지정 or 자동 탐색
    if len(sys.argv) > 1:
        txt_path = Path(sys.argv[1]).expanduser()
        if not txt_path.exists():
            print(f"❌ 파일 없음: {txt_path}")
            sys.exit(1)
        print(f"📄 녹취 파일: {txt_path.name}")
    else:
        txt_path = pick_txt_file(downloads)

    # 2) 과목 선택
    detected = detect_subject(txt_path, subjects) if txt_path else None
    subject = pick_subject(subjects, detected)

    if not subject:
        print("❌ 과목 선택 취소")
        sys.exit(0)

    print(f"\n✅ 과목: {subject}")
    subj_conf = subjects[subject]
    semester_folder = subj_conf["semester_folder"]

    # 3) 강의자료 목록 출력
    materials_dir = semester_base / semester_folder / "강의자료"
    print(f"\n📂 {subject}/강의자료/ (Claude.ai 업로드 참고)")
    show_materials(materials_dir)

    # 4) 녹취 파일 → 녹취/ 폴더로 이동
    if txt_path and txt_path.exists():
        nok_dir = semester_base / semester_folder / "녹취"
        nok_dir.mkdir(exist_ok=True)
        dst = nok_dir / txt_path.name
        shutil.move(str(txt_path), str(dst))
        print(f"\n📥 녹취 파일 이동 완료: 녹취/{txt_path.name}")
    else:
        print("\n⚠️  녹취 파일 없이 진행합니다.")

    # 5) Claude.ai 프로젝트 열기
    claude_url = subj_conf.get("claude_url", "").strip()
    if claude_url:
        print(f"\n🌐 Claude.ai [{subject}] 프로젝트 열기...")
        subprocess.run(["open", claude_url])
    else:
        print(f"\n⚠️  Claude.ai URL 미설정 → setup.py를 실행해서 URL을 등록하세요.")
        print("   직접 claude.ai 에서 해당 과목 프로젝트를 여세요.")

    print("\n" + "─" * 50)
    print("  ✨ 준비 완료!")
    print("  Claude.ai에서 노트 생성 후 HTML을 Downloads에 저장하면")
    print("  watch.py가 자동으로 처리합니다.")
    print("─" * 50)


if __name__ == "__main__":
    main()
