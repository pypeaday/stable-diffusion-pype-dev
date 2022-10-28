import json
import pickle
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
        # necessary for automatic1111 cause there's 4 possible directories between outputs and the actual image
        for _pic in Path(pics_root).glob("**/*.png"):
            if _pic.name == self.name:
                self.source_png_path = _pic
                break
        if self.source == "AUTOMATIC1111":
            self.repo_png_path = Path("AUTOMATIC1111-images", self.name)
        elif self.source == "InvokeAI":
            raise NotImplementedError
        self.repo_webp_path = Path("static", Path(self.name).with_suffix(".webp"))

    def delete(self):
        # delete the file
        if self.repo_png_path.exists():
            # if there's no image then unlink won't work. This might happen if an image gets deleted but the entry didn't get removed from source_app_map somehow
            self.repo_png_path.unlink()
        else:
            pass
            # breakpoint()
        if self.source_png_path.exists():
            # also make sure to try to remove the png in this repo
            self.source_png_path.unlink()
        if self.repo_webp_path.exists():
            # also make sure to try to remove the web in static
            self.repo_webp_path.unlink()
        else:
            pass
        # remove it from source_app_map
        source_app_map.pop(self.name)
        # re-create the file
        with open("source_app_map.json", "w") as f:
            json.dump(source_app_map, f)


def serialize_image_containers():
    try:
        images = pickle.load(open("image_cleaning.pkl", "rb"))
        return [x for x in images if x.name not in source_app_map_golden.keys()]

    except:
        print("failed loading pickle")
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

        pickle.dump(images, open("image_cleaning.pkl", "wb"))
        return images


if __name__ == "__main__":
    images = serialize_image_containers()
    for image in images:
        try:
            image.path
        except AttributeError:
            # if image.path doesn't exist then something is wrong with the SOURCE image not being there
            image.delete()
            continue
        # open the image
        if not Path(image.path).exists():
            # need to re-pickle otherwise next time we'll get FileNotFoundErrors
            pickle.dump(
                [x for x in images if x.name != image.name],
                open("image_cleaning.pkl", "wb"),
            )
            continue

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
                # need to re-pickle otherwise next time we'll just load up images we already decided to keep
                pickle.dump(
                    [x for x in images if x.name != image.name],
                    open("image_cleaning.pkl", "wb"),
                )
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
