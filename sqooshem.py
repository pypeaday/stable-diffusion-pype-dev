import os
from pathlib import Path
from subprocess import Popen

from dotenv import load_dotenv

load_dotenv()

# glob for all png in the outputs repo
autos_files = list(
    Path(f"{os.environ['AUTOMATIC1111_ROOT']}/outputs/").glob("**/*.png")
)

# glob for all files that have been converted
converted_images = list(Path("./static").glob("*.webp"))

# list of files to delete if I have deleted them from $AUTOMATIC1111_ROOT/outputs
webp_to_delete = [
    x for x in converted_images if x.stem not in [y.stem for y in autos_files]
]

# list of files that need to be converted to webp
png_to_convert = [
    x for x in autos_files if x.stem not in [y.stem for y in converted_images]
]


for file in webp_to_delete:
    print(f"deleting {file.name}")
    file.unlink()

for file in png_to_convert:

    cmd = (
        """npx @squoosh/cli --webp '{"quality":70,"target_size":0,"target_PSNR":0,"method":4,"sns_strength":50,"filter_strength":60,"filter_sharpness":0,"filter_type":1,"partitions":0,"segments":4,"pass":1,"show_compressed":0,"preprocessing":0,"autofilter":0,"partition_limit":0,"alpha_compression":1,"alpha_filtering":1,"alpha_quality":100,"lossless":0,"exact":0,"image_hint":0,"emulate_jpeg_size":0,"thread_level":0,"low_memory":0,"near_lossless":100,"use_delta_palette":0,"use_sharp_yuv":0}' """
        + f'"{str(file)}"'  # need filename in quotes since AUTOMATIC1111's images have spaces in name
        + " --output-dir static"
    )
    proc = Popen(cmd, shell=True)
    proc.wait()
