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
        color_dict = {v: k for k, v in st.data_color_value.items()}
        target = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
        return color_dict.get(target, None)

    def save_as_image(self, arr, path, **options) -> None:
        image = Image.new("RGBA", (self.arr_size_x, self.arr_size_y), (20, 255, 0, 0))
        draw = ImageDraw.Draw(image)
        for canvas_x in range(self.arr_size_x):
            for canvas_y in range(self.arr_size_y):
                draw.line(
                    (canvas_x, canvas_y, canvas_x, canvas_y),
                    fill=self.get_data_color(arr[canvas_y][canvas_x]),
                )

        if options.get("to_png"):
            image.save(path, "PNG")

        if options.get("is_end"):
            return

        buffor = BytesIO()
        image.save(buffor, "PNG")
        buffor.seek(0)
        image_buffor = Image.open(buffor)
        self.pix_map = image_buffor.load()

    def generate_mixture(self, file=0) -> None:
        corner_editable = st.corner
        hyperbole = st.hyperbole

        for y in range(self.arr_size_y):
            self.array_[y] = np.random.choice(
                st.pattern_types, self.arr_size_y, p=st.probability
            )
            if y < st.corner and corner_editable > 0:
                self.array_[y][:corner_editable] = ["void"] * (corner_editable)
                self.array_[y][-corner_editable:] = ["void"] * (corner_editable)
                hyperbole -= st.power
                corner_editable -= math.ceil(math.pow(hyperbole, 2))
            if (
                y > (self.arr_size_x - st.up_corner_limit - st.corner)
                and corner_editable <= st.corner
            ):
                hyperbole += -st.power
                corner_editable += math.ceil(math.pow(hyperbole, 2))
                self.array_[y][:corner_editable] = ["void"] * (corner_editable)
                self.array_[y][-corner_editable:] = ["void"] * (corner_editable)

        if not os.path.exists(st.path_mixture):
            os.makedirs(st.path_mixture)
        if not os.path.exists(st.path_generation):
            os.makedirs(st.path_generation)

        return self.save_as_image(
            self.array_, f"{st.path_mixture}/pre_{st.filename}_{file}.png", to_png=True,
        )

