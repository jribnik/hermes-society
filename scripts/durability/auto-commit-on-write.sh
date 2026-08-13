#!/bin/sh
# auto-commit-on-write — close "write-but-don't-commit" with a mechanism, not memory.
#
# Triggered by launchd (ai.hermes.society-autocommit) via WatchPaths (filesystem
# change) and a StartInterval backstop sweep. Idempotent: no staged changes ->
# no commit, so it is a no-op between writes.
#
# Division of labor with the existing post-commit hook:
#   this script COMMITS  (a write becomes durable at creation)
#   the hook      PUSHES (a commit becomes durable at origin)
# Persistence is now a side effect of the write, not an act of remembering.

set -u
REPO="${HERMES_SOCIETY_REPO:-$HOME/.hermes/society}"
GIT="${HERMES_GIT:-/usr/bin/git}"
LOG="$HOME/Library/Logs/hermes-society-autocommit.log"
LOCK="$HOME/Library/Logs/hermes-society-autocommit.lock"

mkdir -p "$HOME/Library/Logs" 2>/dev/null

# --- lock: mkdir is atomic; recover a stale lock from a crashed run (>10 min) ---
if ! mkdir "$LOCK" 2>/dev/null; then
  if [ -d "$LOCK" ] && [ -n "$(find "$LOCK" -mmin +10 2>/dev/null)" ]; then
    rm -rf "$LOCK" && mkdir "$LOCK" 2>/dev/null || exit 0
  else
    exit 0
  fi
fi
trap 'rm -rf "$LOCK" 2>/dev/null' EXIT INT TERM

# --- debounce: let an in-flight multi-file write settle before staging ---
sleep 2

[ -d "$REPO/.git" ] || exit 0
cd "$REPO" || exit 0

# --- stage everything (respects .gitignore: reflections/, escalations/ excluded) ---
"$GIT" add -A 2>/dev/null

# --- idempotency: nothing staged -> done, no empty commit ---
if "$GIT" diff --cached --quiet 2>/dev/null; then
  exit 0
fi

count=$("$GIT" diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
summary=$("$GIT" diff --cached --name-only 2>/dev/null | head -8 | tr '\n' ' ')
msg="auto-commit: ${summary}"
[ "$count" -gt 8 ] 2>/dev/null && msg="${msg}(+$((count - 8)) more)"

if "$GIT" commit -q -m "$msg" 2>>"$LOG"; then
  echo "$(date -u '+%FT%TZ') committed ${count} file(s):${summary}" >> "$LOG"
fi
exit 0
