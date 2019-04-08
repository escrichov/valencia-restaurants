#!/bin/bash

DIRECTORY=.


cd $DIRECTORY
git fetch
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")
if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
    ONLY_BUILD_IF_DATA_CHANGES=True pipenv run python main.py
    exit 1
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    git pull
    ONLY_BUILD_IF_DATA_CHANGES=False pipenv run python main.py
    exit 1
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
    exit 1
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
