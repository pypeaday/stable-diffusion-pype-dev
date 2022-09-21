# stable-diffusion-pype-dev

[![PyPI - Version](https://img.shields.io/pypi/v/stable-diffusion-pype-dev.svg)](https://pypi.org/project/stable-diffusion-pype-dev)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stable-diffusion-pype-dev.svg)](https://pypi.org/project/stable-diffusion-pype-dev)

-----

**Table of Contents**

- [Usage](#usage)
- [Installation](#installation)
- [License](#license)

## Usage

Images and logs need to be copied into stable-diffusion-pype-dev from
stable-diffusion for the image gallery to work.

Assuming you have the stable-diffusion and stable-diffusion-pype-dev repos next
to each other, edit `refresh-and-push.sh` with appropaite paths and then it syncs the
the 2 relevant logs with prompt data as well as all the images that are
generated into this repo.

Then `python sqooshem.py` will sqoosh pngs into webp format (pngs are gitignored)

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
