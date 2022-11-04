# stable-diffusion-pype-dev

[Check it out here!](https://pypeaday.github.io/stable-diffusion-pype-dev/)

[![PyPI - Version](https://img.shields.io/pypi/v/stable-diffusion-pype-dev.svg)](https://pypi.org/project/stable-diffusion-pype-dev)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stable-diffusion-pype-dev.svg)](https://pypi.org/project/stable-diffusion-pype-dev)

-----

**Table of Contents**

- [Deps](#Dependencies)
- [Usage](#usage)
- [Installation](#installation)
- [License](#license)

## Note

Only supporting AUTOMATIC1111's web ui right now

!! I recommend for my gallery to be smooth to go into AUTOMATIC1111's web ui
settings and disable jpg saving. Otherwise you can convert jpgs to png as
discussed below

## Dependencies


Some of the settings in AUTOMATIC1111's web ui save files as .jpg but
`sqooshem.py` I originally wrote only for .png files. So you can use
`ImageMagick` to automatically convert all .jpg to .png, then the rest happens
automagically

`sudo apt install imagemagick`

## Usage

The setup for this workflow is not really ideal but small-enough scale that it works out OK...

1. Assuming a parent directory for git repos, say `~/git`
2. Clone repos as follows:

```bash
cd ~/git

git clone https://github.com/pypeaday/stable-diffusion-pype-dev.git

# I list my fork of invoke-ai/InvokeAI's repo because on my branch nic are some
# requirements fixes for my python setup -> this is improtant for a filepath later
# git clone https://github.com/invoke-ai/InvokeAI.git
<!-- git clone https://github.com/pypeaday/stable-diffusion.git -->
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git

```

2a. In `stable-diffusion-pype-dev` you'll need a few files made or renamed:
    * `.env` -> I include `.env.example` that you can just rename to `.env` and configure the paths for `AUTOMATIC1111_ROOT` and `INVOKEAI_ROOT`
    * `source_app_map.json` needs to be a blank json file at first -> you can just rename `source_app_map.json.example` to `source_app_map.json`
    * same story for `source_app_map_golden.json`

3. Setup the stable-diffusion application repos as you wish - this isn't a
   guide supplementing either of their setup instructions at all

4. Run `sqooshem.py` which will log to `source_app_map.json` where each image (by full path) came from and sqoosh the png into a webp and put that in `static`

> source_app_map.json is in place of a database just to get me going -> eventually I'll put a little sqlite thing together

# NOTE 

I have a streamlit app coming for filtering out images you don't want in your
gallery. For now if you need this functionality you can use
`interactive_clean.py` which will just iterate through pictures one at a time,
and ask if you want to keep it or not. If you type `y` then the image is logged
to `source_app_map_golden.json` and if you type `n` then the image (source and
webp if it's been sqooshed) will be deleted, including the prompt file from
AUTOMATIC1111 if it exists, or if it's from InvokeAI's webui then the
corresponding line in the prompt file will also be deleted... It'll be as if
that image never existed

The following command will get you a markata site with images and commands displayed!

```console
pipx run hatch run clean-serve
```

## Installation

```console
pip install .  # no package published
```

## License

`stable-diffusion-pype-dev` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
