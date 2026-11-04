#!/usr/bin/env python3
"""bible_fetch.py — thin wrapper. 실제 구현(정본)은 ~/Developer/bible-tools/bible_fetch.py (모든 프로젝트 공용).
기존 호출자(`from bible_fetch import ...`, CLI)는 그대로 동작한다. 파서를 여기서 다시 만들지 않는다."""
import importlib.util
import os
import sys

_SHARED = os.path.join(os.path.expanduser("~"), "Developer", "bible-tools", "bible_fetch.py")
if not os.path.isfile(_SHARED):
    raise ImportError(f"공용 bible-tools 없음: {_SHARED}")
_spec = importlib.util.spec_from_file_location("bible_fetch_shared", _SHARED)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["bible_fetch_shared"] = _mod
_spec.loader.exec_module(_mod)
globals().update({k: v for k, v in vars(_mod).items() if not k.startswith("__")})

if __name__ == "__main__":
    sys.exit(_mod.main(sys.argv[1:]))
