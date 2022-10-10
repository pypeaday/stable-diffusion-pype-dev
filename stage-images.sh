#!/bin/bash

rsync -r /home/nic/personal/stable-diffusion/outputs/img-samples/ InvokeAI-images

cp /home/nic/personal/stable-diffusion/outputs/img-samples/dream_log.txt dream_log.txt
cp /home/nic/personal/stable-diffusion/outputs/img-samples/dream_web_log.txt dream_web_log.txt

# these images come from AUTOMATIC1111's webui, the filenames are the prompts
rsync -r /home/nic/third-party/stable-diffusion-webui/outputs/txt2img-images/ AUTOMATIC1111-images
rsync -r /home/nic/third-party/stable-diffusion-webui/outputs/txt2img-grids/ AUTOMATIC1111-images

# replace spaces in jpg files with _ for converting to png
for f in AUTOMATIC1111-images/*.jpg
do
  new="${f// /_}"
  if [ "$new" != "$f" ]
  then
    if [ -e "$new" ]
    then
      echo not renaming \""$f"\" because \""$new"\" already exists
    else
      echo moving "$f" to "$new"
    mv "$f" "$new"
  fi
fi
done

# convert .jpg to .png for sqooshing

ls -1 AUTOMATIC1111-images/*.jpg | xargs -n 1 bash -c 'convert "$0" "${0%.jpg}.png"'

python sqooshem.py
