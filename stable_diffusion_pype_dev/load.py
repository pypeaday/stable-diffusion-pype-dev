"""prompt loader"""
import json
from pathlib import Path

from markata.hookspec import hook_impl, register_attr

from .models import AUTOMATIC1111WebPrompt

# from .models import WebPrompt, Prompt

with open("source_app_map.json", "r") as f:
    source_app_map = json.load(f)


@hook_impl
def configure(markata) -> None:
    markata.content_directories = [Path("static")]


def _turn_original_png_path_to_static_webp_path(filepath: str):

    return Path("static", Path(Path(filepath).name)).with_suffix(".webp")


@hook_impl
@register_attr("articles")
def load(markata) -> None:
    # articles should be type: List[Union[AUTOMATIC1111WebPrompt, Prompt, WebPrompt]]
    markata.articles = []
    # prompts = Path("dream_log.txt").read_text().split("\n")
    # markata.articles += [
    #     Prompt(_turn_original_png_path_to_static_webp_path(pair[0]), pair[1])
    #     for p in prompts
    #     if len(pair := p.split(":")) == 2
    # ]

    # prompts = Path("dream_web_log.txt").read_text().split("\n")
    # web_based_articles: List[WebPrompt] = []
    # for p in prompts:
    #     if len(pair := p.split(":")) == 16:
    #         file, raw_data = (
    #             _turn_original_png_path_to_static_webp_path(pair[0]),
    #             pair[1:],
    #         )
    #         data = json.loads(":".join(raw_data))
    #         web_based_articles.append(WebPrompt(file, data))

    automatic1111_data = (
        # regardless of which suboutput folder the source images are in, I store them flat in static - so just check for the webp version of the picture in this repo
        Path("static", Path(Path(k).name).with_suffix(".webp"))
        for k, v in source_app_map.items()
        if v == "AUTOMATIC1111"
    )
    automatic1111_articles = [AUTOMATIC1111WebPrompt(f) for f in automatic1111_data]

    # markata.articles += web_based_articles
    markata.articles += automatic1111_articles
