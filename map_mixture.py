import os
import json
import sys
import math

from PIL import Image, ImageDraw
from io import BytesIO
import numpy as np


config = json.load(open('config.json'))
gen = int(config["gen"])
path_generation = f'{config["path_mixture"]}_{gen}'
filename = f'pre_{config["filename"]}'
pattern_types = config['types']
pattern_probability = config['probability']
quality = int(config['mixture_quality'])

# ==
get_data_base_by_type = config["get_data_base_by_type"]
get_data_base_by_color = config["get_data_base_by_color"]
# ==

print(sys.argv[0])


class Generate_Map_Mixture:
    def __init__(self):
        self.arr_size_x, self.arr_size_y = config["arr_size"], config["arr_size"]
        self.array_ = np.full(
            (self.arr_size_x, self.arr_size_y), "...............")
        self.pix_map

        self.corner = int(config['arr_size']/3.3)
        self.corner_ = self.corner
        self.up_corner_limit = - \
            math.log(config['arr_size'], 2) - \
            math.log(config['arr_size'], 2) - 1
        self.hyper_bol = -2.1
        self.power = -0.03

    def getcolor(self, c):
        return get_data_base_by_type.get(c, '#ffffff')

    def getvalue(self, arg):
        target = '#{:02x}{:02x}{:02x}'.format(arg[0], arg[1], arg[2])
        return get_data_base_by_color.get(target, None)

    def save_as_image(self, arr, path, **options):
        im = Image.new(
            'RGBA', (self.arr_size_x, self.arr_size_y), (20, 255, 0, 0))
        draw = ImageDraw.Draw(im)
        for dx in range(self.arr_size_x):
            for dy in range(self.arr_size_y):
                draw.line((dx, dy, dx, dy), fill=self.getcolor(arr[dy][dx]))

        if options.get('to_png'):
            im.save(path, 'PNG')

        buffor = BytesIO()
        # replace buffor to 'file.png' if you want convert to image
        im.save(buffor, 'PNG')
        buffor.seek(0)

        img_buf = Image.open(buffor)
        self.pix_map = img_buf.load()

    def generate(self, file):
        for y in range(self.arr_size_y):
            self.array_[y] = np.random.choice(
                pattern_types, self.arr_size_y, p=pattern_probability)
            if y < self.corner and self.corner_ > 0:
                self.array_[y][:self.corner_] = ['void']*(self.corner_)
                self.array_[y][-self.corner_:] = ['void']*(self.corner_)
                self.hyper_bol -= self.power
                self.corner_ -= math.ceil(math.pow(self.hyper_bol, 2))
            if y > (self.arr_size_x - self.up_corner_limit - self.corner) and self.corner_ <= self.corner:
                self.hyper_bol += -self.power
                self.corner_ += math.ceil(math.pow(self.hyper_bol, 2))
                self.array_[y][:self.corner_] = ['void']*(self.corner_)
                self.array_[y][-self.corner_:] = ['void']*(self.corner_)
        if not os.path.exists(path_generation):
            os.makedirs(path_generation)
        return self.save_as_image(self.array_, f'{path_generation}/{filename}_{file}.png', to_png=True)


map = Generate_Map_Mixture()
map.generate(1)
