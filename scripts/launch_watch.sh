#!/bin/bash
# launch_watch.sh — watch.py를 새 터미널 창에서 실행
#
# 사용법:
#   bash scripts/launch_watch.sh
#
# 맥북 시작 시 자동 실행하려면:
#   bash scripts/launch_watch.sh --install
#   (launchd에 등록 → 로그인 시 자동 시작)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LN_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON="$(which python3)"
PLIST_NAME="com.lecturnote.watch"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

start_in_terminal() {
  echo "🖥  새 터미널 창에서 watch.py 시작..."
  osascript << APPLESCRIPT
tell application "Terminal"
  do script "echo \"👁  강의노트 감시 시작\" && cd '$LN_ROOT' && $PYTHON scripts/watch.py"
  activate
end tell
APPLESCRIPT
  echo "✅ 터미널 창이 열렸습니다."
}

install_launchd() {
  echo "📋 launchd 에이전트 설치 중..."

  # plist 생성
  cat > "$PLIST_PATH" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$PLIST_NAME</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$LN_ROOT/scripts/watch.py</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$LN_ROOT</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$HOME/Library/Logs/lecture-watch.log</string>
  <key>StandardErrorPath</key>
  <string>$HOME/Library/Logs/lecture-watch-error.log</string>
</dict>
</plist>
PLIST

  # 기존 에이전트 언로드 후 재등록
  launchctl unload "$PLIST_PATH" 2>/dev/null
  launchctl load -w "$PLIST_PATH"

  echo "✅ launchd 등록 완료 — 로그인 시 자동 시작됩니다."
  echo ""
  echo "  로그 확인: tail -f ~/Library/Logs/lecture-watch.log"
  echo "  중지:      launchctl unload $PLIST_PATH"
  echo "  재시작:    launchctl unload $PLIST_PATH && launchctl load -w $PLIST_PATH"
}

uninstall_launchd() {
  if [ -f "$PLIST_PATH" ]; then
    launchctl unload "$PLIST_PATH" 2>/dev/null
    rm "$PLIST_PATH"
    echo "✅ launchd 에이전트 제거 완료"
  else
    echo "설치된 launchd 에이전트가 없습니다."
  fi
}

case "${1:-}" in
  --install)   install_launchd ;;
  --uninstall) uninstall_launchd ;;
  *)           start_in_terminal ;;
esac
