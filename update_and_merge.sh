git fetch origin main
git checkout main
git reset --hard origin/main
git branch -D my-new-branch || true
git checkout -b my-new-branch
