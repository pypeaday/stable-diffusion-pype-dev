# stable-diffusion-pype-dev

[Check it out here!](https://pypeaday.github.io/stable-diffusion-pype-dev/)

[![PyPI - Version](https://img.shields.io/pypi/v/stable-diffusion-pype-dev.svg)](https://pypi.org/project/stable-diffusion-pype-dev)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stable-diffusion-pype-dev.svg)](https://pypi.org/project/stable-diffusion-pype-dev)

-----

**Table of Contents**

- [Usage](#usage)
- [Installation](#installation)
- [License](#license)

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
git clone https://github.com/pypeaday/stable-diffusion.git
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git

```

3. Setup the stable-diffusion application repos as you wish - this isn't a
   guide supplementing either of their setup instructions at all
4. To combine outputs from invoke-ai's console app, their webapp, and AUTOMATIC1111's webapp reference my `refresh-and-push` script and use as is appropriate for you

    summary: It basically copies images and prompt files from the Invoke-AI repo setup to stable-diffusion-pype-dev so that `load.py` can create markata articles appropriately from images from either entrypoint of the model
    It also copies AUTOMATIC1111's images into their own ignored directory
    because of the process flow of `sqoosh` which re-encodes all the `png`
    images into `webp` for storage. Those images are named after their prompts
    though, which is a different saving model than the other project, so
    `sqooshem.py` takes that into account and the `refresh-and-push` script
    moves things around appropriately

The following command will get you a markata site with images and commands displayed!

```console
pipx run hatch run build-serve
```

## Installation

```console
pip install .  # no package published
```

## License

`stable-diffusion-pype-dev` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
