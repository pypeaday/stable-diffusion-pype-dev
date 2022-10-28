import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image as PillowImage

with open("source_app_map.json", "r") as f:
    source_app_map = json.load(f)


pics_root = "/home/nic/third-party/stable-diffusion-webui/outputs/"


@dataclass
class Image:

    name: str

    def __post_init__(self):
        # stupidedly glob over all the files to find this one
        for _pic in Path(pics_root).glob("**/*.png"):
            if _pic.name == self.name:
                self.path = _pic
                break

    def delete(self, nopath: bool = False):
        # delete the file
        if not nopath:
            # if there's no image then unlink won't work. This might happen if an image gets deleted but the entry didn't get removed from source_app_map somehow
            self.path.unlink()
        # also make sure to try to remove the webp in this repo
        for _pic in Path("./AUTOMATIC1111-images").glob("*.webp"):
            if _pic.name == self.name:
                print(f"deleting {_pic.name}")
                _pic.unlink()
        # remove it from source_app_map
        source_app_map.pop(self.name)
        # re-create the file
        with open("source_app_map.json", "w") as f:
            json.dump(source_app_map, f)


if __name__ == "__main__":
    images = []
    for pic, source in source_app_map.items():
        if source == "AUTOMATIC1111":
            images.append(Image(pic))
            ...
        else:
            ...
    for image in images:
        try:
            image.path
        except AttributeError:
            image.delete(nopath=True)
            continue
        with PillowImage.open(image.path) as im:
            im.show()
            keep = input("Keep? ")
            if "n" in keep.lower():
                image.delete()
        im.close()
