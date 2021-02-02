import os
import sys
from typing import Dict

import settings as settings
from map_mixture import MapMixtureGenerator


def progressbar(iterator, prefix="", size=60, file=sys.stdout):
    count = len(iterator)

    def show(progress):
        level_on_scale = int(size * progress / count)
        file.write(
            f"{prefix}[{'#' * level_on_scale}{'.' * (size - level_on_scale)}] {progress}/{count}\r"
        )
        file.flush()

    show(0)

    for progress, item in enumerate(iterator):
        yield item
        show(progress + 1)
    file.write("\n")
    file.flush()


def get_data_value(color) -> str:
    color_dict = {v: k for k, v in settings.DATA_COLOR_VALUE.items()}
    target = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

    return color_dict.get(target, None)


class MapGenerator(MapMixtureGenerator):
    def __init__(self):
        super().__init__()
        self.arr2D = None
        self.point_x = None
        self.point_y = None

    def run(self):
        for file_number in range(0, settings.NUMBER_FILES):
            self.generate_mixture(file_number)
            self.create_pixel_map()

            for index in progressbar(
                range(settings.QUALITY), f"Quality progress - image {file_number}: ", 40
            ):
                for y in range(self.arr_size_y):
                    for x in range(self.arr_size_x):
                        self.find_grid_value(x, y, self.array_)

            if not os.path.exists(settings.PATH_GENERATION):
                os.makedirs(settings.PATH_GENERATION)

            self.process_image(
                self.array_,
                f"{settings.PATH_GENERATION}/{settings.FILENAME}_{file_number}.png",
                to_png=True,
                is_end=True,
            )

    def create_pixel_map(self) -> None:
        for y in range(self.arr_size_y):
            for x in range(self.arr_size_x):
                self.array_[y][x] = get_data_value(self.pix_map[x, y])

    def replace_on_grid(self, po_y, po_x, tg_y, tg_x) -> None:
        value_target = self.arr2D[tg_y][tg_x]

        self.arr2D[tg_y][tg_x] = self.arr2D[po_y][po_x]
        self.arr2D[po_y][po_x] = value_target

    def get_corner(self, corner, points=False, distance=1) -> Dict[str, str]:
        top_or_bottom = distance if corner[0] == "t" else -distance
        right_or_left = distance if corner[1] == "r" else -distance

        if corner[0] == ".":
            top_or_bottom = 0
        if corner[1] == ".":
            right_or_left = 0

        corner_dict = {}

        try:
            value = self.arr2D[self.point_y + top_or_bottom][
                self.point_x + right_or_left
            ]
            corner_dict.update({"value": value})
        except IndexError:
            return {"value": None}

        if points:
            corner_dict.update(
                {
                    "cordinate": {
                        "y": self.point_y + top_or_bottom,
                        "x": self.point_x + right_or_left,
                    }
                }
            )
        return corner_dict

    def check_two_edges(self, material) -> bool:
        """Check minimum two similar values over the edge"""

        return (
            self.get_corner(".l").get("value") == material
            or self.get_corner(".r").get("value") == material
        ) and (
            self.get_corner("b.").get("value") == material
            or self.get_corner("t.").get("value") == material
        )

    def find_grid_value(self, point_x, point_y, arr2D):
        self.arr2D = arr2D
        self.point_x = point_x
        self.point_y = point_y

        for material in settings.TYPES_TO_GROUP:
            if self.get_corner("..").get("value") != material or self.check_two_edges(
                material
            ):
                continue

            check_number = {"repeat": 0, "vector": 0}

            for quality_rang in range(settings.MOVE_QUALITY):
                check_number["vector"] = 0

                for corner_vector in settings.CORNER_TYPES:
                    if self.get_corner(corner_vector).get("value") == material:
                        continue

                    for it in range(2, settings.FIND_AROUND_RANGE):
                        if (
                            self.get_corner(corner_vector, distance=it).get("value")
                            == material
                        ):
                            check_number["vector"] = self.get_corner(
                                corner_vector, points=True, distance=it - 1
                            ).get("cordinate")
                            break

                    if check_number.get("vector") != 0:
                        pos = check_number.get("vector")
                        self.replace_on_grid(
                            point_y, point_x, pos.get("y"), pos.get("x")
                        )


if __name__ == "__main__":
    try:
        settings.GENERATION_NUMBER = int(sys.argv[1])
    except IndexError:
        print("Index Error generation number - settings generation_number")

    try:
        settings.NUMBER_FILES = int(sys.argv[2])
    except IndexError:
        print("Index Error number of files")

    new_map = MapGenerator().run()
