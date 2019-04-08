#!/bin/bash
export PATH=$PATH:/usr/local/bin

git fetch
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")
if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
    ONLY_BUILD_IF_DATA_CHANGES=True pipenv run python main.py
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    git pull
    ONLY_BUILD_IF_DATA_CHANGES=False pipenv run python main.py
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
    git pull
    git push
    exit 1
else
    echo "Git Error"
    exit 1
fi
git add -A
git commit -m "Sync"
git push
