from pathlib import Path
from subprocess import Popen

files = Path("InvokeAI-images").glob("*.png")
autos_files = Path("AUTOMATIC111-images").glob("*.png")


for file in files:

    if (
        Path(str(file).replace("InvokeAI-images", "static"))
        .with_suffix(".webp")
        .exists()
    ):
        continue
    cmd = (
        """npx @squoosh/cli --webp '{"quality":70,"target_size":0,"target_PSNR":0,"method":4,"sns_strength":50,"filter_strength":60,"filter_sharpness":0,"filter_type":1,"partitions":0,"segments":4,"pass":1,"show_compressed":0,"preprocessing":0,"autofilter":0,"partition_limit":0,"alpha_compression":1,"alpha_filtering":1,"alpha_quality":100,"lossless":0,"exact":0,"image_hint":0,"emulate_jpeg_size":0,"thread_level":0,"low_memory":0,"near_lossless":100,"use_delta_palette":0,"use_sharp_yuv":0}' """
        + f"'{str(file)}'"  # need filename in quotes since AUTOMATIC111's images have spaces in name
        + " --output-dir static"
    )
    proc = Popen(cmd, shell=True)
    proc.wait()

for file in autos_files:
    if (
        Path(str(file).replace("AUTOMATIC111-images", "static"))
        .with_suffix(".webp")
        .exists()
    ):
        continue
    cmd = (
        """npx @squoosh/cli --webp '{"quality":70,"target_size":0,"target_PSNR":0,"method":4,"sns_strength":50,"filter_strength":60,"filter_sharpness":0,"filter_type":1,"partitions":0,"segments":4,"pass":1,"show_compressed":0,"preprocessing":0,"autofilter":0,"partition_limit":0,"alpha_compression":1,"alpha_filtering":1,"alpha_quality":100,"lossless":0,"exact":0,"image_hint":0,"emulate_jpeg_size":0,"thread_level":0,"low_memory":0,"near_lossless":100,"use_delta_palette":0,"use_sharp_yuv":0}' """
        + f"'{str(file)}'"  # need filename in quotes since AUTOMATIC111's images have spaces in name
        # + " --output-dir static"
        + " --output-dir static"
    )
    proc = Popen(cmd, shell=True)
    proc.wait()
