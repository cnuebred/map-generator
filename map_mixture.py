import math
import os
from io import BytesIO

import numpy as np
from PIL import Image, ImageDraw

import settings as st


def get_data_color(value) -> str:
    return st.DATA_COLOR_VALUE.get(value, "#ffffff")


class MapMixtureGenerator:
    def __init__(self) -> None:
        self.arr_size_x, self.arr_size_y = st.ARR_SIZE, st.ARR_SIZE
        self.array_ = np.full((self.arr_size_x, self.arr_size_y), "void", dtype="U15")
        self.pix_map = None
        self.corner_scale = st.CORNER
        self.hyperbole = st.HYPERBOLE

    def _draw_on_image(self, arr):
        for canvas_x in range(self.arr_size_x):
            for canvas_y in range(self.arr_size_y):
                self.draw.line(
                    (canvas_x, canvas_y, canvas_x, canvas_y),
                    fill=get_data_color(arr[canvas_y][canvas_x]),
                )

    def _generate_buffor(self, image):
        buffor = BytesIO()
        image.save(buffor, "PNG")
        buffor.seek(0)
        image_buffor = Image.open(buffor)
        self.pix_map = image_buffor.load()

    def process_image(self, arr, path, **options) -> None:
        image = Image.new("RGBA", (self.arr_size_x, self.arr_size_y), (20, 255, 0, 0))
        self.draw = ImageDraw.Draw(image)

        self._draw_on_image(arr)

        if options.get("to_png"):
            image.save(path, "PNG")

        if options.get("is_end"):
            return

        self._generate_buffor(image)

    def generate_mixture(self, file=0) -> None:

        for y in range(self.arr_size_y):
            self.array_[y] = np.random.choice(
                st.PATTERN_TYPES, self.arr_size_y, p=st.PROBABILITY
            )

            def replace_pixels():
                self.array_[y][: self.corner_scale] = ["void"] * self.corner_scale
                self.array_[y][-self.corner_scale :] = ["void"] * self.corner_scale

            def calculate_corners_variables(operator=1) -> None:
                self.hyperbole += st.POWER
                self.corner_scale += math.ceil(self.hyperbole ** 2) * operator

            if y < st.CORNER and self.corner_scale > 0:
                replace_pixels()
                calculate_corners_variables(-1)
            if (
                y > (self.arr_size_x - st.UP_CORNER_LIMIT - st.CORNER)
                and self.corner_scale <= st.CORNER
            ):
                calculate_corners_variables()
                replace_pixels()

        if not os.path.exists(st.PATH_MIXTURE):
            os.makedirs(st.PATH_MIXTURE)

        if not os.path.exists(st.PATH_GENERATION):
            os.makedirs(st.PATH_GENERATION)

        return self.process_image(
            self.array_, f"{st.PATH_MIXTURE}/pre_{st.FILENAME}_{file}.png", to_png=True,
        )
