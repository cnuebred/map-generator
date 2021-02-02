import math
import pathlib
from io import BytesIO

import numpy as np
from PIL import Image, ImageDraw

import settings


def get_data_color(value) -> str:
    return settings.DATA_COLOR_VALUE.get(value, settings.DEFAULT_COLOR)


class MapMixtureGenerator:
    def __init__(self) -> None:
        self.arr_size_x, self.arr_size_y = settings.ARR_SIZE, settings.ARR_SIZE
        self.array_ = np.full((self.arr_size_x, self.arr_size_y), "void", dtype="U15")
        self.corner_scale = settings.CORNER
        self.hyperbole = settings.HYPERBOLE
        self.pix_map = None

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
                settings.PATTERN_TYPES, self.arr_size_y, p=settings.PROBABILITY
            )

            def replace_pixels():
                self.array_[y][: self.corner_scale] = ["void"] * self.corner_scale
                self.array_[y][-self.corner_scale :] = ["void"] * self.corner_scale

            def calculate_corners_variables(operator=1) -> None:
                self.hyperbole += settings.POWER
                self.corner_scale += math.ceil(self.hyperbole ** 2) * operator

            if y < settings.CORNER and self.corner_scale > 0:
                replace_pixels()
                calculate_corners_variables(-1)
            if (
                y > (self.arr_size_x - settings.UP_CORNER_LIMIT - settings.CORNER)
                and self.corner_scale <= settings.CORNER
            ):
                calculate_corners_variables()
                replace_pixels()

        pathlib.Path(settings.PATH_MIXTURE).mkdir(parents=True, exist_ok=True)

        pathlib.Path(settings.PATH_GENERATION).mkdir(parents=True, exist_ok=True)

        return self.process_image(
            self.array_,
            f"{settings.PATH_MIXTURE}/pre_{settings.FILENAME}_{file}.png",
            to_png=True,
        )
