#!/usr/bin/env bash
# Push this repository to GitHub.
#
#   ./scripts/publish_to_github.sh git@github.com:<owner>/<repo>.git
#
# Requirements: git, and credentials for the target remote (SSH key or token).
set -euo pipefail

REMOTE="${1:-}"
if [[ -z "$REMOTE" ]]; then
  echo "usage: $0 <git-remote-url>" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> running the quality gate before publishing"
python3 scripts/validate_repo.py --repo .

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE"
else
  git remote add origin "$REMOTE"
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
echo "==> pushing to $REMOTE ($BRANCH)"
git push -u origin "$BRANCH"
echo "==> done"
