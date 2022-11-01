import json
from dataclasses import dataclass
from pathlib import Path

""" 

        self.published = True
        self.title = self.file.name
        self.slug = self.file.name.replace(",", "-").replace(".", "-").replace(" ", "-")
        self.app_source = "automatic1111"
        self.prompt_file_path = Path(self.file).with_suffix(".txt")

        self.prompt: str
        self.params: dict
        self.width: str
        self.height: str
"""


@dataclass
class Prompt:
    file: Path
    command: str

    def __post_init__(self):
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
    file: Path
    data: dict

    def __post_init__(self):

        self.published = True
        self.title = self.file.name
        self.slug = self.file.name
        self.prompt = self.data["prompt"]
        self.height = self.data["height"]
        self.width = self.data["width"]
        self.command = json.dumps(self.data)
        self.app_source = "dream-web"

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
