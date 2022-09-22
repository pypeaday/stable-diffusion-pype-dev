#!/bin/bash

./stage-images.sh

git add ./dream_log.txt
git add ./dream_web_log.txt

git add ./static

git commit -m "regular update"

git push
