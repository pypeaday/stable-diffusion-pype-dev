"""prompt loader"""
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from markata.hookspec import hook_impl, register_attr

with open("source_app_map.json", "r") as f:
    source_app_map = json.load(f)


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


@dataclass
class AUTOMATIC1111WebPrompt:
    file: Path

    def __post_init__(self):

        self.published = True
        self.title = self.file.name
        self.slug = self.file.name
        self.prompt = self.file.name
        self.height = None
        self.width = None
        self.command = self.file.name
        self.app_source = "automatic1111"

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


@hook_impl
def configure(markata) -> None:
    markata.content_directories = [Path("static")]


def _turn_original_png_path_to_static_webp_path(filepath: str):

    return Path("static", Path(Path(filepath).name)).with_suffix(".webp")


@hook_impl
@register_attr("articles")
def load(markata) -> None:
    prompts = Path("dream_log.txt").read_text().split("\n")
    markata.articles = [
        Prompt(_turn_original_png_path_to_static_webp_path(pair[0]), pair[1])
        for p in prompts
        if len(pair := p.split(":")) == 2
    ]

    prompts = Path("dream_web_log.txt").read_text().split("\n")
    web_based_articles: List[WebPrompt] = []
    for p in prompts:
        if len(pair := p.split(":")) == 16:
            file, raw_data = (
                _turn_original_png_path_to_static_webp_path(pair[0]),
                pair[1:],
            )
            data = json.loads(":".join(raw_data))
            web_based_articles.append(WebPrompt(file, data))

    automatic1111_data = (
        Path("static", Path(k).with_suffix(".webp"))
        for k, v in source_app_map.items()
        if v == "AUTOMATIC1111"
    )
    automatic1111_articles = [AUTOMATIC1111WebPrompt(f) for f in automatic1111_data]

    markata.articles += web_based_articles
    markata.articles += automatic1111_articles
