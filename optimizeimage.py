from PIL import Image, ImageFilter
from pathlib import Path
from os import listdir
import os
from os.path import isfile, join, split, basename
import requests
import shutil
import hashlib


# https://engineeringblog.yelp.com/2017/06/making-photos-smaller.html


THUMBNAIL_SIZE = 512, 512


def thumbnail_image(filename, thumbnail_size):
    # Read image
    im = Image.open(filename)

    # Generate thumbnail
    im.thumbnail(thumbnail_size, Image.ANTIALIAS)
    data = list(im.getdata())

    # Remove exif data
    im_without_exif = Image.new(im.mode, im.size)
    im_without_exif.putdata(data)

    # Save new image
    im_without_exif.save(filename, "JPEG", optimize=True, quality=85, progressive=True)


def convert_to_jpg(in_filename, out_filename):
    # Read image
    im = Image.open(in_filename)

    # Convert to jpg
    im = im.convert('RGB')
    im.save(out_filename)


def download_image(url, path):
    response = requests.get(url, stream=True)
    with open(path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


def optimize_url(url, download_dir):
    _, extension = os.path.splitext(url)
    extension = extension.lower()
    if extension == '.jpeg':
        extension = '.jpg'
    filename = join(download_dir, hashlib.md5(url.encode('utf-8')).hexdigest())
    filename = f'{filename}-{THUMBNAIL_SIZE[0]}x{THUMBNAIL_SIZE[1]}'
    download_path = filename + extension
    cache_path = filename + '.jpg'
    if not os.path.exists(cache_path):
        download_image(url, download_path)
        if download_path != cache_path:
            convert_to_jpg(download_path, cache_path)
            os.remove(download_path)

        thumbnail_image(cache_path, THUMBNAIL_SIZE)

    return cache_path
