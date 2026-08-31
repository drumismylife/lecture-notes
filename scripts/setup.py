#!/usr/bin/env python3
"""
setup.py — 최초 1회 실행
Claude.ai 프로젝트 URL 설정 + watchdog 의존성 설치

사용법:
  python3 scripts/setup.py
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPTS_DIR / "config.json"


def install_deps():
    print("\n📦 의존성 설치 중 (watchdog)...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "watchdog", "--quiet"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("   ✅ watchdog 설치 완료")
    else:
        print("   ⚠️  설치 실패:", result.stderr.strip())
        print("   직접 실행: pip install watchdog")


def setup_urls(config):
    subjects = config["subjects"]
    print("\n🔗 Claude.ai 프로젝트 URL 설정")
    print("   각 과목 프로젝트를 열고 주소창 URL을 복사해서 붙여넣으세요.")
    print("   Enter → 건너뛰기 / 기존 URL 유지\n")

    for subj, conf in subjects.items():
        current = conf.get("claude_url", "")
        if current:
            print(f"  [{subj}] 현재: {current}")
            new_url = input(f"    새 URL (Enter=유지): ").strip()
        else:
            new_url = input(f"  [{subj}] URL: ").strip()

        if new_url:
            conf["claude_url"] = new_url

    return config


def setup_notebooklm(config):
    """과목별 NotebookLM 노트북 연결. 없으면 nlm으로 즉석 생성 가능."""
    subjects = config["subjects"]
    print("\n📓 NotebookLM 노트북 연결")
    print("   매주 배포된 강의노트를 자동으로 NotebookLM 소스로 올립니다.")
    print("   Enter → 건너뛰기(비연동) / n → 지금 새 노트북 생성 / 기존 ID 붙여넣기\n")

    for subj, conf in subjects.items():
        current = conf.get("notebook_id", "")
        if current:
            print(f"  [{subj}] 연동됨: {current}")
            continue

        answer = input(f"  [{subj}] 노트북 ID (n=새로 생성, Enter=건너뛰기): ").strip()
        if not answer:
            continue
        if answer.lower() == "n":
            label = conf.get("semester", "")
            title = f"{subj}" + (f" — {label}" if label else "")
            result = subprocess.run(
                ["nlm", "notebook", "create", title, "--json"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                try:
                    notebook = json.loads(result.stdout)
                    new_id = notebook.get("id") or notebook.get("notebook_id")
                except json.JSONDecodeError:
                    new_id = None
                if new_id:
                    conf["notebook_id"] = new_id
                    print(f"    ✅ 노트북 생성: {title} ({new_id})")
                else:
                    print(f"    ⚠️  노트북 ID 파싱 실패 — 출력 확인 필요: {result.stdout[:200]}")
            else:
                print(f"    ❌ 노트북 생성 실패: {result.stderr.strip()[:200]}")
        else:
            conf["notebook_id"] = answer

    return config


def verify_paths(config):
    paths = config["paths"]
    print("\n📂 경로 확인")
    for key, val in paths.items():
        expanded = Path(val).expanduser()
        exists = "✅" if expanded.exists() else "❌ 없음"
        print(f"  {exists}  {key}: {expanded}")


def main():
    print("⚙️  강의노트 자동화 초기 설정")
    print("=" * 45)

    if CONFIG_PATH.exists():
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        print("기존 config.json을 불러왔습니다.")
    else:
        print("❌ config.json이 없습니다. scripts/ 폴더를 확인하세요.")
        sys.exit(1)

    install_deps()
    config = setup_urls(config)
    config = setup_notebooklm(config)
    verify_paths(config)

    CONFIG_PATH.write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n✅ 설정 저장 완료: {CONFIG_PATH}")
    print("\n─── 이제 이렇게 쓰세요 ──────────────────────")
    print("  수업 후 준비:  python3 scripts/prepare.py")
    print("  감시 시작:     python3 scripts/watch.py")
    print("────────────────────────────────────────────")


if __name__ == "__main__":
    main()
