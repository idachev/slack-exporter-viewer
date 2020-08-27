import math
import os

from PIL import Image

thumb_suffix = [64, 80, 160, 360, 480, 720, 800, 960, 1024]

priv_file_path = 'files.slack.com/files-pri/'

tmb_dir = '/files-tmb/'


def convert_to_thumb(org_img, thumb_size, dst_img):
    im = Image.open(org_img)

    size = (thumb_size, thumb_size)
    if thumb_size > 160:
        if im.width > im.height:
            new_height = math.ceil((im.width / im.height) * thumb_size)
            size = (thumb_size, new_height)
        else:
            new_width = math.ceil((im.height / im.width) * thumb_size)
            size = (new_width, thumb_size)

    im.thumbnail(size)

    dst_dir = os.path.dirname(dst_img)
    os.makedirs(dst_dir, exist_ok=True)

    im.save(dst_img)


def slack_build_thumb(files_path, img_path):
    f_path = os.path.join(files_path, img_path)
    if os.path.isfile(f_path):
        return

    index = img_path.index(tmb_dir)
    if index == -1:
        return

    img_name = os.path.basename(img_path)
    img_base_name, img_ext = os.path.splitext(img_name)

    base_thumb_name = None
    found_thumb = None
    for thumb_iter in thumb_suffix:
        thumb_iter_str = '_' + str(thumb_iter)
        if img_base_name.endswith(thumb_iter_str):
            found_thumb = thumb_iter
            base_thumb_name = img_base_name[:-1*len(thumb_iter_str)]
            break

    if not base_thumb_name:
        return

    dir_img_thumb = img_path[index + len(tmb_dir):-1*(len(img_name) + 1)]
    dt_index = dir_img_thumb.rindex('-')
    if dt_index <= 0:
        return

    priv_dir = dir_img_thumb[0:dt_index]

    org_img = os.path.join(files_path, priv_file_path, priv_dir, base_thumb_name + img_ext)
    if not os.path.isfile(org_img):
        return

    convert_to_thumb(org_img, found_thumb, os.path.join(files_path, img_path))
