#!/bin/bash

DIRECTORY=.
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

cd $DIRECTORY
if [ $LOCAL = $REMOTE ]; then
    ONLY_BUILD_IF_DATA_CHANGES=True pipenv run python main.py
elif [ $LOCAL = $BASE ]; then
    git pull
    ONLY_BUILD_IF_DATA_CHANGES=False pipenv run python main.py
else
    echo "Git Error"
    exit 1
fi
git add -A
git commit -m "Sync"
git push
