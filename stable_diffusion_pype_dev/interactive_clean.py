import json
import pickle
from dataclasses import dataclass
from pathlib import Path

from PIL import Image as PillowImage

with open("source_app_map.json", "r") as f:
    source_app_map = json.load(f)

with open("source_app_map_golden.json", "r") as f:
    source_app_map_golden = json.load(f)


automatic1111_pics_root = "/home/nic/third-party/stable-diffusion-webui/outputs/"
invokeai_pics_root = "/home/nic/personal/stable-diffusion/outputs/"


AUTOMATIC1111_IMAGES = [im for im in Path(automatic1111_pics_root).glob("**/*.png")]
INVOKEAI_IMAGES = [im for im in Path(invokeai_pics_root).glob("**/*.png")]


@dataclass
class Image:

    file: Path
    source: str

    def __post_init__(self):
        # stupidedly glob over all the files to find this one
        # necessary for automatic1111 cause there's 4 possible directories between outputs and the actual image

        self.repo_webp_path = Path("static", Path(self.file.name).with_suffix(".webp"))

    def delete(self):
        if self.file.exists():
            # also make sure to try to remove the png in this repo
            self.file.unlink()
        if self.repo_webp_path.exists():
            # also make sure to try to remove the web in static
            self.repo_webp_path.unlink()
        else:
            pass
        # remove it from source_app_map
        source_app_map.pop(str(self.file))
        # re-create the file
        with open("source_app_map.json", "w") as f:
            json.dump(source_app_map, f)


def serialize_image_containers():
    try:
        images = pickle.load(open("image_cleaning.pkl", "rb"))
        return [x for x in images if str(x.file) not in source_app_map_golden.keys()]

    except:
        print("failed loading pickle")
        images = []
        # loop over all tracked pics (pngs) and source (automatic1111 or invokeai)
        for pic, source in source_app_map.items():
            # if I decided to keep it, pass
            if pic in source_app_map_golden.keys():
                print(f"Already keeping {pic} in golden list")
                continue
            # # create data structure for ease
            # elif source == "AUTOMATIC1111":
            #     # source as variable in case I can actually use this dataclass easily for both automatic1111 and invokeAI
            #     images.append(Image(pic, source))
            #     ...
            # elif source == "InvokeAI":
            #     # for InvokeAI repo images
            #     ...
            # else:
            #     breakpoint()
            images.append(Image(Path(pic), source))

        pickle.dump(images, open("image_cleaning.pkl", "wb"))
        return images


if __name__ == "__main__":
    images = serialize_image_containers()
    for image in images:
        try:
            image.file
        except AttributeError:
            # if image.source_png_path doesn't exist then something is wrong with the SOURCE image not being there
            print(f"would delete {image.file.name}")
            # image.delete()
            continue
        # open the image
        if not Path(image.file).exists():
            print(f"{image.file} source png does not exist")
            # need to re-pickle otherwise next time we'll get FileNotFoundErrors
            pickle.dump(
                [x for x in images if x.file.name != image.file.name],
                open("image_cleaning.pkl", "wb"),
            )
            continue

        with PillowImage.open(image.file) as im:
            im.show()
            keep = input("Keep? ")
            if "n" in keep.lower():
                # delete the source png, the webp in static, and the record in source_app_map_golden
                # note: automatic1111 doesn't store prompt history, it is the filename. InvokeAI DOES store between a couple different text files to be aware of
                image.delete()

            elif "y" in keep.lower():
                source_app_map_golden[str(image.file)] = image.source
                with open("source_app_map_golden.json", "w") as f:
                    json.dump(source_app_map_golden, f)
                # need to re-pickle otherwise next time we'll just load up images we already decided to keep
                print("remaking pickle")
                pickle.dump(
                    [x for x in images if str(x.file) != str(image.file)],
                    open("image_cleaning.pkl", "wb"),
                )
            else:
                print(f"No decision made - passing on {image.file.name}")
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
