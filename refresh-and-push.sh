#!/bin/bash

# ./stage-images.sh

# git add ./dream_log.txt
# git add ./dream_web_log.txt
python ./sqooshem.py

git add ./static
git add ./source_app_map.json

git commit -m "regular update"

git push
