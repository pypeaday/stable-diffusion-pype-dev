"""module for processing images out of AUTOMATIC1111's repo"""

import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


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
        self.prompt = self.path.name
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
