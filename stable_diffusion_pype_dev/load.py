"""prompt loader"""
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from markata.hookspec import hook_impl, register_attr

from .models import AUTOMATIC1111WebPrompt

# source env variables
load_dotenv()


@hook_impl
def configure(markata) -> None:
    markata.content_directories = [Path("static")]


@hook_impl
@register_attr("articles")
def load(markata) -> None:
    markata.articles: List[AUTOMATIC1111WebPrompt] = []

    converted_images = list(Path("./static").glob("*.webp"))

    markata.articles = [AUTOMATIC1111WebPrompt(f) for f in converted_images]
