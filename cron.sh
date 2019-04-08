#!/bin/bash

DIRECTORY=.

cd $DIRECTORY
git pull
pipenv run python main.py
git add -A
git commit -m "Sync"
git push
