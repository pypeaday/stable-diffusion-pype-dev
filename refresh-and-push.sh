#!/bin/bash


rsync -r /home/nic/personal/stable-diffusion/outputs/img-samples/ static
cp /home/nic/personal/stable-diffusion/outputs/img-samples/dream_log.txt dream_log.txt
cp /home/nic/personal/stable-diffusion/outputs/img-samples/dream_web_log.txt dream_web_log.txt

python sqooshem.py

git add ./dream_log.txt
git add ./dream_web_log.txt
rm -rf static/*.png  # idk why I need this.. something messed up
git add ./static

git commit -m "regular update"

git push
