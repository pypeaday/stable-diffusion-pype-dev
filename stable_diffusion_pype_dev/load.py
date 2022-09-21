"""prompt loader"""
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

from markata.hookspec import hook_impl, register_attr


@dataclass
class Prompt:
    file: Path
    command: str
    status: str = "published"

    def __post_init__(self):
        self.title = self.file.name
        self.webp = self.file.with_suffix(".webp")
        self.slug = self.file.name
        self.prompt = self.command.split('"')[1]
        self.params = {p[1]: p[2:] for p in self.command.split('"')[2].split()}
        self.height = self.params["H"]
        self.width = self.params["W"]

    def __getitem__(self, key):
        return self.to_dict()[key]

    def keys(self):
        return self.to_dict().keys()

    def to_dict(self):
        return vars(self)


@dataclass
class WebPrompt:
    file: Path
    data: dict
    status: str = "published"

    def __post_init__(self):
        self.title = self.file.name
        self.webp = self.file.with_suffix(".webp")
        self.slug = self.file.name
        self.prompt = self.data["prompt"]
        self.height = self.data["height"]
        self.width = self.data["width"]
        self.command = json.dumps(self.data)

    def __getitem__(self, key):
        return self.to_dict()[key]

    def keys(self):
        return self.to_dict().keys()

    def to_dict(self):
        return vars(self)


@hook_impl
def configure(markata) -> None:
    markata.content_directories = [Path("static")]


@hook_impl
@register_attr("articles")
def load(markata) -> None:
    prompts = Path("dream_log.txt").read_text().split("\n")
    markata.articles = [
        Prompt(Path(pair[0]), pair[1])
        for p in prompts
        if len(pair := p.split(":")) == 2
    ]

    prompts = Path("dream_web_log.txt").read_text().split("\n")
    web_based_articles: List[Prompt] = []
    for p in prompts:
        if len(pair := p.split(":")) == 16:
            file, raw_data = Path(pair[0]), pair[1:]
            data = json.loads(":".join(raw_data))
            web_based_articles.append(WebPrompt(file, data))

    markata.articles += web_based_articles
