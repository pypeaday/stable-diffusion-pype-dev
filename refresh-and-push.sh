#!/bin/bash


rsync -r /home/nic/personal/stable-diffusion/outputs/img-samples/ InvokeAI-images

cp /home/nic/personal/stable-diffusion/outputs/img-samples/dream_log.txt dream_log.txt
cp /home/nic/personal/stable-diffusion/outputs/img-samples/dream_web_log.txt dream_web_log.txt

# these images come from AUTOMATIC111's webui, the filenames are the prompts
rsync -r /home/nic/third-party/stable-diffusion-webui/outputs/txt2img-images/ AUTOMATIC111-images

python sqooshem.py

rsync -r AUTOMATIC111-images/*.webp static

git add ./dream_log.txt
git add ./dream_web_log.txt
rm -rf static/*.png  # idk why I need this.. something messed up

git add ./static

git commit -m "regular update"

git push
