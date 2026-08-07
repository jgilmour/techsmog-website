#!/bin/bash
cd "$(dirname "$0")"

echo "=== Cleaning up git lock files ==="
rm -f .git/index.lock .git/HEAD.lock .git/packed-refs.lock \
      .git/refs/heads/main.lock .git/refs/heads/zz-lock-test.lock \
      .git/objects/maintenance.lock 2>/dev/null
git branch -D zz-lock-test zz2 2>/dev/null || true
rm -f zz-scratch-test.txt 2>/dev/null
git gc --prune=now

echo ""
echo "=== Pushing to origin/main ==="
git push origin main

echo ""
echo "=== Done! Press any key to close ==="
read -n 1
