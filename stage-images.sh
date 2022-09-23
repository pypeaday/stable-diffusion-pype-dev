#!/bin/bash

rsync -r /home/nic/personal/stable-diffusion/outputs/img-samples/ InvokeAI-images

cp /home/nic/personal/stable-diffusion/outputs/img-samples/dream_log.txt dream_log.txt
cp /home/nic/personal/stable-diffusion/outputs/img-samples/dream_web_log.txt dream_web_log.txt

# these images come from AUTOMATIC1111's webui, the filenames are the prompts
rsync -r /home/nic/third-party/stable-diffusion-webui/outputs/txt2img-images/ AUTOMATIC1111-images
rsync -r /home/nic/third-party/stable-diffusion-webui/outputs/txt2img-grids/ AUTOMATIC1111-images

python sqooshem.py
