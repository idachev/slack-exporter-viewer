import math
import os

from PIL import Image

thumb_suffix = [64, 80, 160, 360, 480, 720, 800, 960, 1024]

priv_file_path = 'files.slack.com/files-pri/'

tmb_dir = '/files-tmb/'
download_path = '/download/'


def reduce_img_size(width, height, to_size, min_sq_size=160):
    size = (width, height)

    if width <= min_sq_size or height <= min_sq_size:
        return size

    size = (to_size, to_size)

    if to_size > min_sq_size:
        if width > height:
            new_height = math.ceil((height / width) * to_size)
            size = (to_size, new_height)
        else:
            new_width = math.ceil((width / height) * to_size)
            size = (new_width, to_size)

    return size


def convert_to_thumb(org_img, thumb_size, dst_img):
    im = Image.open(org_img)

    size = reduce_img_size(im.width, im.height, thumb_size)
    im.thumbnail(size)

    dst_dir = os.path.dirname(dst_img)
    os.makedirs(dst_dir, exist_ok=True)

    im.save(dst_img)


def slack_get_priv_path(img_path):
    index = img_path.find(tmb_dir)
    if index == -1:
        return None, None

    img_name = os.path.basename(img_path)
    img_base_name, img_ext = os.path.splitext(img_name)

    base_thumb_name = None
    found_thumb = None
    for thumb_iter in thumb_suffix:
        thumb_iter_str = '_' + str(thumb_iter)
        if img_base_name.endswith(thumb_iter_str):
            found_thumb = thumb_iter
            base_thumb_name = img_base_name[:-1 * len(thumb_iter_str)]
            break

    if not base_thumb_name:
        return None, None

    dir_img_thumb = img_path[index + len(tmb_dir):-1 * (len(img_name) + 1)]
    dt_index = dir_img_thumb.rindex('-')
    if dt_index <= 0:
        return None, None

    priv_dir = dir_img_thumb[0:dt_index]

    return os.path.join(priv_file_path, priv_dir, base_thumb_name + img_ext), found_thumb


def slack_build_thumb(files_path, img_path):
    f_path = os.path.join(files_path, img_path)
    if os.path.isfile(f_path):
        return

    priv_path, found_thumb = slack_get_priv_path(img_path)

    if priv_path is None:
        return

    org_img = os.path.join(files_path, priv_path)
    if not os.path.isfile(org_img):
        return

    convert_to_thumb(org_img, found_thumb, os.path.join(files_path, img_path))


def slack_check_download(files_path, img_path):
    f_path = os.path.join(files_path, img_path)
    if os.path.isfile(f_path):
        return img_path

    index = img_path.find(download_path)
    if index == -1:
        return img_path

    nodwn_img_path = img_path[0:index] + img_path[index + len(download_path):]
    f_nodown_path = os.path.join(files_path, nodwn_img_path)
    if os.path.isfile(f_nodown_path):
        return nodwn_img_path

    return img_path
