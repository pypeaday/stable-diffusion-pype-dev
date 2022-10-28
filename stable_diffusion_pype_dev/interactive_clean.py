import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image as PillowImage

with open("source_app_map.json", "r") as f:
    source_app_map = json.load(f)

with open("source_app_map_golden.json", "r") as f:
    source_app_map_golden = json.load(f)


pics_root = "/home/nic/third-party/stable-diffusion-webui/outputs/"


@dataclass
class Image:

    name: str
    source: str

    def __post_init__(self):
        # stupidedly glob over all the files to find this one
        for _pic in Path(pics_root).glob("**/*.png"):
            if _pic.name == self.name:
                self.path = _pic
                break

    def delete(self):
        # delete the file
        try:
            # if there's no image then unlink won't work. This might happen if an image gets deleted but the entry didn't get removed from source_app_map somehow
            self.path.unlink()
        except Exception:
            breakpoint()
        try:
            # also make sure to try to remove the png in this repo
            Path("AUTOMATIC1111-images", self.path.name).unlink()
        except Exception:
            breakpoint()
        try:
            # also make sure to try to remove the web in static
            Path("static", Path(self.path.name).with_suffix(".webp")).unlink()
        except Exception:
            breakpoint()
        # remove it from source_app_map
        source_app_map.pop(self.name)
        # re-create the file
        with open("source_app_map.json", "w") as f:
            json.dump(source_app_map, f)


if __name__ == "__main__":
    images = []
    # loop over all tracked pics (pngs) and source (automatic1111 or invokeai)
    for pic, source in source_app_map.items():
        # if I decided to keep it, pass
        if pic in source_app_map_golden.keys():
            print(f"Already keeping {pic} in golden list")
            continue
        # create data structure for ease
        elif source == "AUTOMATIC1111":
            # source as variable in case I can actually use this dataclass easily for both automatic1111 and invokeAI
            images.append(Image(pic, source))
            ...
        elif source == "InvokeAI":
            # for InvokeAI repo images
            ...
        else:
            breakpoint()
    for image in images:
        try:
            image.path
        except AttributeError:
            # if image.path doesn't exist then something is wrong with the SOURCE image not being there
            image.delete()
            continue
        # open the image
        with PillowImage.open(image.path) as im:
            im.show()
            keep = input("Keep? ")
            if "n" in keep.lower():
                # delete the source png, the webp in static, and the record in source_app_map_golden
                # note: automatic1111 doesn't store prompt history, it is the filename. InvokeAI DOES store between a couple different text files to be aware of
                image.delete()
            elif "y" in keep.lower():
                source_app_map_golden[image.name] = image.source
                with open("source_app_map_golden.json", "w") as f:
                    json.dump(source_app_map_golden, f)
            else:
                print(f"No decision made - passing on {image.name}")
        im.close()

    # # Trying to delete webp images that made it into static but aren't either tracked in any prompt OR especially if they aren't in golden repo
    # all_images = {**source_app_map, **source_app_map_golden}
    # breakpoint()
    # for webp in Path("static").glob("*.webp"):
    #     png_path = Path(webp.name).with_suffix(".png")
    #     if png_path not in all_images.keys():
    #         if all_images[png_path.name] == "InvokeAI":
    #             continue
    #         print(webp.name)
    #         with PillowImage.open(str(webp)) as im:
    #             im.show()
    #             keep = input("Keep? ")
    #             if "n" in keep.lower():
    #                 webp.unlink()
