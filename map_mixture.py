from io import BytesIO
import subprocess
import os
import json
import sys
from PIL import Image, ImageDraw
import numpy as np
import math


config = json.load(open('config.json'))

arr_size_x, arr_size_y = config["arr_size"], config["arr_size"]
gen = int(config["gen"])
path_generation = f'{config["path_mixture"]}_{gen}'
filename = f'pre_{config["filename"]}'
#path_new_generation = f'{config["path_new_gen"]}{gen}'
number_files = 1

pattern_types = config['types']
pattern_probability = config['probability']
quality = int(config['mixture_quality'])

# ==
get_data_base_by_type = config["get_data_base_by_type"]
# ==

print(sys.argv[0])


def getcolor(c):
    return get_data_base_by_type.get(c, '#ffffff')


array_ = np.full((arr_size_x, arr_size_y), "...............")


def save_as_image(arr, path):
    im = Image.new('RGBA', (arr_size_x, arr_size_y), (20, 255, 0, 0))
    draw = ImageDraw.Draw(im)
    for dx in range(arr_size_x):
        for dy in range(arr_size_y):
            draw.line((dx, dy, dx, dy), fill=getcolor(arr[dy][dx]))

    im.save(path, 'PNG')
    buffor = BytesIO()
    # replace buffor to 'file.png' if you want convert to image
    im.save(buffor, 'PNG')
    buffor.seek(0)

    img_buf = Image.open(buffor)
    pix_map = img_buf.load()
    return pix_map


#corner = 16
#corner_ = 4
#up_corner_limit = 5
#hyper_bol = 1
#power = -0.3

corner = int(config['arr_size']/3.3)
corner_ = corner
up_corner_limit = - \
    math.log(config['arr_size'], 2) - math.log(config['arr_size'], 2) - 1
hyper_bol = -2.1
power = -0.03


def generate():
    global corner_
    global hyper_bol
    # corner_ = 3
    # hyper_bol = 1

    for file in range(0, number_files):
        for y in range(arr_size_y):
            array_[y] = np.random.choice(
                pattern_types, arr_size_y, p=pattern_probability)
            if y < corner and corner_ > 0:
                array_[y][:corner_] = ['void']*(corner_)
                array_[y][-corner_:] = ['void']*(corner_)
                hyper_bol -= power
                corner_ -= math.ceil(math.pow(hyper_bol, 2))
            if y > (arr_size_x - up_corner_limit - corner) and corner_ <= corner:
                hyper_bol += -power
                corner_ += math.ceil(math.pow(hyper_bol, 2))
                array_[y][:corner_] = ['void']*(corner_)
                array_[y][-corner_:] = ['void']*(corner_)
        if not os.path.exists(path_generation):
            os.makedirs(path_generation)
        return save_as_image(array_, f'{path_generation}/{filename}_{file}.png')


# generate()

# subprocess.run(['python', 'map_new_generation.py', f'{gen}',
#                 f'{number_files}'], capture_output=False)
