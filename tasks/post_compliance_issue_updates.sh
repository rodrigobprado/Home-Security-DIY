#!/usr/bin/env bash
set -euo pipefail

DIR="tasks/issue-comments"
ISSUES=(102 103 104 105 106 107 108)

for n in "${ISSUES[@]}"; do
  f="$DIR/$n.md"
  if [ ! -f "$f" ]; then
    echo "SKIP #$n (arquivo ausente: $f)"
    continue
  fi

  ok=0
  for t in 1 2 3 4 5; do
    if gh issue comment "$n" --body-file "$f" >/tmp/issue_comment_${n}.out 2>/tmp/issue_comment_${n}.err; then
      ok=1
      break
    fi
    sleep $((t * 2))
  done

  if [ "$ok" -eq 1 ]; then
    echo "OK #$n $(cat /tmp/issue_comment_${n}.out)"
  else
    echo "ERR #$n"
    cat /tmp/issue_comment_${n}.err || true
  fi
done
