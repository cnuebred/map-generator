import json
import math
import os
import sys
from io import BytesIO

import numpy as np
from PIL import Image, ImageDraw

import settings as st


class GenerateMapMixture:
    def __init__(self) -> None:
        self.arr_size_x, self.arr_size_y = st.arr_size, st.arr_size
        self.array_ = np.full((self.arr_size_x, self.arr_size_y), "void", dtype="U15")
        self.pix_map = None

    def get_data_color(self, value) -> str:
        return st.data_color_value.get(value, "#ffffff")

    def get_data_value(self, color) -> str:
        target = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
        return st.data_color_value.get(target, None)

    def save_as_image(self, arr, path, **options) -> None:
        image = Image.new("RGBA", (self.arr_size_x, self.arr_size_y), (20, 255, 0, 0))
        draw = ImageDraw.Draw(image)
        for dx in range(self.arr_size_x):
            for dy in range(self.arr_size_y):
                draw.line((dx, dy, dx, dy), fill=self.get_data_color(arr[dy][dx]))

        if options.get("to_png"):
            image.save(path, "PNG")

        if options.get("end"):
            return

        buffor = BytesIO()
        image.save(buffor, "PNG")
        buffor.seek(0)
        image_buffor = Image.open(buffor)
        self.pix_map = image_buffor.load()

    def generate_mixture(self, file=0) -> None:
        corner_ = st.corner
        hyper_bol = st.hyper_bol

        for y in range(self.arr_size_y):
            self.array_[y] = np.random.choice(
                st.pattern_types, self.arr_size_y, p=st.probability
            )
            if y < st.corner and corner_ > 0:
                self.array_[y][:corner_] = ["void"] * (corner_)
                self.array_[y][-corner_:] = ["void"] * (corner_)
                hyper_bol -= st.power
                corner_ -= math.ceil(math.pow(hyper_bol, 2))
            if (
                y > (self.arr_size_x - st.up_corner_limit - st.corner)
                and corner_ <= st.corner
            ):
                hyper_bol += -st.power
                corner_ += math.ceil(math.pow(hyper_bol, 2))
                self.array_[y][:corner_] = ["void"] * (corner_)
                self.array_[y][-corner_:] = ["void"] * (corner_)

        if not os.path.exists(st.path_mixture):
            os.makedirs(st.path_mixture)
        if not os.path.exists(st.path_generation):
            os.makedirs(st.path_generation)

        return self.save_as_image(
            self.array_, f"{st.path_mixture}/pre_{st.filename}_{file}.png", to_png=True,
        )

