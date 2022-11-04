"""module for processing images out of AUTOMATIC1111's repo"""

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image

# source env variables
load_dotenv()


@dataclass
class AUTOMATIC1111WebPrompt:
    file: Path

    def __post_init__(self):

        self.published = True
        self.title = self.file.name
        self.slug = self.file.name.replace(",", "-").replace(".", "-").replace(" ", "-")
        self.app_source = "automatic1111"
        self.prompt_file_path = Path(self.file).with_suffix(".txt")

        self.prompt: str
        self.params: dict
        self.width: str
        self.height: str

        if self.prompt_file_path.exists():
            self._setup_params_from_file()
        else:
            self._setup_params_without_file()

    def _setup_params_from_file(self):
        """
        example content of prompt file:
        Big Bang Creation Space Galaxies, atmospheric, hyper realistic, 8k, epic composition, cinematic, octane render, artstation cosmic  photography, 16K resolution, 8k resolution, detailed space painting by Ivan Shishkin, DeviantArt, Flickr, rendered in Enscape, Miyazaki, Nausicaa Ghibli, 4k detailed post processing, trending on artstation, rendering by octane, unreal engine, UDR, UHD
        Steps: 20, Sampler: PLMS, CFG scale: 23.5, Seed: 2415897950, Size: 1024x1024
        """
        self.prompt, raw_params = self.prompt_file_path.read_text().split("\n")
        self.params = json.dumps(
            {l.split(":")[0]: l.split(":")[1].strip() for l in raw_params.split(", ")}
        )  # noqa
        # example: '{"Steps": "20", "Sampler": "PLMS", "CFG scale": "23.5", "Seed": "2415897950", "Size": "1024x1024"}'  # noqa: E501
        self.height, self.width = self.params["Size"].split("x")

    def _setup_params_without_file(self):
        """ """
        self.prompt = self.file.name
        with Image.open(str(self.file)) as im:
            self.width = im.width
            self.height = im.height
        self.params = {}

    def __getitem__(self, key, default):
        return self.to_dict().get(key, default)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def keys(self):
        return self.to_dict().keys()

    def to_dict(self):
        return vars(self)

    def get(self, key, default=None):
        return self.__getitem__(key, default)

    def delete(self):
        self.file.unlink()
        self.prompt_file_path.unlink(missing_ok=True)


@dataclass
class Prompt:
    file: Path
    command: str

    def __post_init__(self):
        raise NotImplementedError
        self.published = True
        self.title = self.file.name
        self.slug = self.file.name
        self.prompt = self.command.split('"')[1]
        self.params = {p[1]: p[2:] for p in self.command.split('"')[2].split()}
        self.height = self.params["H"]
        self.width = self.params["W"]
        self.app_source = "dream-console"

    def __getitem__(self, key, default):
        return self.to_dict().get(key, default)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def keys(self):
        return self.to_dict().keys()

    def to_dict(self):
        return vars(self)

    def get(self, key, default=None):
        return self.__getitem__(key, default)


@dataclass
class WebPrompt:
    """
    created from a line in InvokeAI's .../outputs/img-samples/dream_web_log.txt
    ex:
    ./outputs/img-samples/000083.2641703450.png:
    {"prompt": "oil painting of steampunk snake drinking coffee",
    "iterations": "1",
    "steps": "50",
    "cfgscale": "7.5",
    "sampler": "k_lms",
    "width": "512",
    "height": "512",
    "seed": "-1",
    "initimg": "",
    "strength": "0.75",
    "fit": "on",
    "gfpgan_strength": "0.8",
    "upscale_level": "",
    "upscale_strength": "0.75"}
    """

    entry: str

    def __post_init__(self):

        self.prompt_file = Path(
            f"{os.environ.get('INVOKEAI_ROOT')}/outputs/img-samples/dream_web_log.txt"
        )
        self.published = True
        self.rel_image_path = entry.split(":")[0]
        _pattern = "{(.*?)}"
        self.raw_params_data = re.findall(_pattern, entry)[0].split(",")
        self.params = {}
        self.title = self.file.name
        self.file = Path(f"{os.environ.get('INVOKEAI_ROOT')}", self.rel_image_path)
        self.slug = self.file.name
        self.prompt = self.data["prompt"]
        self.height = self.data["height"]
        self.width = self.data["width"]
        self.command = json.dumps(self.data)
        self.app_source = "dream-web"

    def strip(l: str) -> str:
        return l.replace('"', "").strip()

    def __getitem__(self, key, default):
        return self.to_dict().get(key, default)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def keys(self):
        return self.to_dict().keys()

    def to_dict(self):
        return vars(self)

    def get(self, key, default=None):
        return self.__getitem__(key, default)

    def _remove_from_prompt_file(self):
        ...

    def delete(self):
        self.file.unlink()
        self._remove_from_prompt_file()
