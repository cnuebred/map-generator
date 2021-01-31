import json
import os
import sys

import numpy as np

import settings as st
from map_mixture import GenerateMapMixture

try:
    gen = int(sys.argv[1])
except IndexError:
    gen = st.gen

try:
    number_files = int(sys.argv[2])
except IndexError:
    number_files = st.number_files


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size * j / count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#" * x, "." * (size - x), j, count))
        file.flush()

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    file.write("\n")
    file.flush()


class Generate_Map_Generation(GenerateMapMixture):
    def __init__(self):
        super().__init__()

    def run(self):
        for file_number in range(0, number_files):
            # image = Image.open(f'{path_generation}/map_generation_r{file}.png')   ## generates from the image
            self.generate_mixture(file_number)  # generates from the buffor
            self.create_pixel_map()
            for x in progressbar(
                range(st.quality), f"Quality progress - image {file_number}: ", 40
            ):
                for y in range(self.arr_size_y):
                    for index, x in enumerate(self.array_[y]):
                        self.find_value_grid(index, y, self.array_, x)

            if not os.path.exists(st.path_generation):
                os.makedirs(st.path_generation)

            self.save_as_image(
                self.array_,
                f"{st.path_generation}/{st.filename}_{file_number}.png",
                to_png=True,
                end=True,
            )

    def create_pixel_map(self) -> None:
        for y in range(self.arr_size_y):
            for x in range(self.arr_size_x):
                self.array_[y][x] = self.get_data_value(self.pix_map[x, y])

    def replace_on_grid(self, po_y, po_x, tg_y, tg_x) -> None:
        value_target = self.arr2D[tg_y][tg_x]
        self.arr2D[tg_y][tg_x] = self.arr2D[po_y][po_x]
        self.arr2D[po_y][po_x] = value_target

    def check_corner(self, corner, points=False, distance=1) -> dict:
        ud = distance if corner[0] == "u" else -distance
        rl = distance if corner[1] == "r" else -distance
        if corner[0] == ".":
            ud = 0
        if corner[1] == ".":
            rl = 0

        if points:
            return {"y": self.point_y + ud, "x": self.point_x + rl}
        try:
            value = self.arr2D[self.point_y + ud][self.point_x + rl]
        except:
            value = False
        return {"value": value}

    def corners_condition(self, material) -> bool:
        return (
            self.check_corner(".l").get("value") == material
            or self.check_corner(".r").get("value") == material
        ) and (
            self.check_corner("d.").get("value") == material
            or self.check_corner("u.").get("value") == material
        )

    def find_value_grid(self, point_x, point_y, arr2D):
        self.arr2D = arr2D
        self.point_x = point_x
        self.point_y = point_y

        for material in st.types_to_group:
            if self.check_corner("..").get("value") != material:
                break

            check_number = {"repeat": 0, "vector": 0}
            if self.corners_condition(material):
                continue
            else:
                for el in range(st.move_quality):
                    check_number["vector"] = 0
                    for corner_vector in [
                        "ul",
                        "ur",
                        "dl",
                        "dr",
                        "u.",
                        ".r",
                        "d.",
                        ".l",
                    ]:
                        if self.check_corner(corner_vector).get("value") == material:
                            continue

                        for it in range(2, st.find_round):
                            if (
                                self.check_corner(corner_vector, distance=it).get(
                                    "value"
                                )
                                == material
                            ):
                                check_number["vector"] = self.check_corner(
                                    corner_vector, distance=it - 1, points=True
                                )
                                break

                        if check_number.get("vector") != 0:
                            pos = check_number.get("vector")
                            self.replace_on_grid(
                                point_y, point_x, pos.get("y"), pos.get("x")
                            )


new_map = Generate_Map_Generation().run()
