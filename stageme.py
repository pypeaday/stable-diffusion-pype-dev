# 1. table with filename, prompt, source app
# 2. spoosh file into webp in static
# 3. markata articles can lookup file in table for source_app as attr on class
import sqlite3
from pathlib import Path
from subprocess import Popen

con = sqlite3.connect("images.db")

cur = con.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS stable_diffusion_images(source_image, webp_image, repo, source_app, prompt, params)"
)


files = Path("InvokeAI-images").glob("*.png")
autos_files = Path("AUTOMATIC1111-images").glob("*.png")

# get all images from InvokeAI-images that have been sqooshed
sqooshed_images_from_invoke_query = cur.execute(
    "SELECT source_image FROM stable_diffusion_images WHERE repo = Invoke-AI;"
)
sqooshed_images_from_invoke_res = sqooshed_images_from_invoke_query.fetchall()

for file in files:
    # todo: check this Syntax
    if str(file) in [r[0] for r in sqooshed_images_from_invoke_res]:
        continue

    # webp file will be in static
    webp_file = Path(str(file).replace("InvokeAI-images", "static")).with_suffix(
        ".webp"
    )

    # sqoosh
    cmd = (
        """npx @squoosh/cli --webp '{"quality":70,"target_size":0,"target_PSNR":0,"method":4,"sns_strength":50,"filter_strength":60,"filter_sharpness":0,"filter_type":1,"partitions":0,"segments":4,"pass":1,"show_compressed":0,"preprocessing":0,"autofilter":0,"partition_limit":0,"alpha_compression":1,"alpha_filtering":1,"alpha_quality":100,"lossless":0,"exact":0,"image_hint":0,"emulate_jpeg_size":0,"thread_level":0,"low_memory":0,"near_lossless":100,"use_delta_palette":0,"use_sharp_yuv":0}' """
        + f"'{str(file)}'"  # need filename in quotes since AUTOMATIC111's images have spaces in name
        + " --output-dir static"
    )

    # wait for sqoosh
    proc = Popen(cmd, shell=True)
    proc.wait()

    # insert row into table for this file - will be updated when markata makes articles
    cur.execute(
        f"""INSERT INTO stable_diffusion_images VALUES ('{str(file)}', {(str(webp_file))}, 'Invoke-AI', '', '', '')"""
    )

    # don't forget to commit
    con.commit()

# get all images from AUTOMATIC1111-images that have been sqooshed
sqooshed_images_from_automatic1111_query = cur.execute(
    "SELECT source_image FROM stable_diffusion_images WHERE repo = AUTOMATIC1111;"
)
sqooshed_images_from_automatic1111_res = (
    sqooshed_images_from_automatic1111_query.fetchall()
)

for file in autos_files:
    # todo: check this Syntax
    if str(file) in [r[0] for r in sqooshed_images_from_automatic1111_res]:
        continue

    # webp file will be in static
    webp_file = Path(str(file).replace("AUTOMATIC1111-images", "static")).with_suffix(
        ".webp"
    )

    # sqoosh
    cmd = (
        """npx @squoosh/cli --webp '{"quality":70,"target_size":0,"target_PSNR":0,"method":4,"sns_strength":50,"filter_strength":60,"filter_sharpness":0,"filter_type":1,"partitions":0,"segments":4,"pass":1,"show_compressed":0,"preprocessing":0,"autofilter":0,"partition_limit":0,"alpha_compression":1,"alpha_filtering":1,"alpha_quality":100,"lossless":0,"exact":0,"image_hint":0,"emulate_jpeg_size":0,"thread_level":0,"low_memory":0,"near_lossless":100,"use_delta_palette":0,"use_sharp_yuv":0}' """
        + f"'{str(file)}'"  # need filename in quotes since AUTOMATIC1111's images have spaces in name
        + " --output-dir static"
    )

    # wait for sqoosh
    proc = Popen(cmd, shell=True)
    proc.wait()

    # insert row into table for this file - will be updated when markata makes articles
    cur.execute(
        f"""INSERT INTO stable_diffusion_images VALUES ('{str(file)}', {(str(webp_file))}, 'AUTOMATIC1111', '', '', '')"""
    )

    # don't forget to commit
    con.commit()

con.close()
