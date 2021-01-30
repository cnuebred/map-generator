import os
from map_mixture import Generate_Map_Mixture
import sys
import json
import numpy as np


# --
config = json.load(open('config.json'))

try:
    gen = int(sys.argv[1])  # int(sys.argv[1])
except:
    gen = int(config["gen"])
try:
    number_files = int(sys.argv[2])  # int(sys.argv[1])
except:
    number_files = int(config["number_files"])

path_generation = f'{config["path_mixture"]}_{gen}'
path_new_generation = f'{config["path_generation"]}_{gen}'
filename = f'{config["filename"]}'


quality = int(config["quality"])
move_quality = int(config["move_quality"])
# --


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" %
                   (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()


class Generate_Map_Generation(Generate_Map_Mixture):
    def __init__(self):
        super().__init__()

        for file_number in range(0, number_files):
            # im = Image.open(f'{path_generation}/map_generation_r{file}.png')   ## generates from the image
            pix = self.generate(gen)  # generates from the buffor
            self.array_ = self.create_pixel_map(pix)
            for x in progressbar(range(quality), f"Quality progress - image {file_number}: ", 40):
                for y in range(self.arr_size_y):
                    for idx, x in enumerate(self.array_[y]):
                        self.find_value_grid(idx, y, self.array_, x)

            if not os.path.exists(path_new_generation):
                os.makedirs(path_new_generation)
            self.save_as_image(
                self.array_, f'{path_new_generation}/{filename}_{file_number}.png', to_png=True, finnal=True)

    def create_pixel_map(self, pix):
        for y in range(self.arr_size_y):
            for x in range(self.arr_size_x):
                self.array_[y][x] = self.get_value_by_color(pix[x, y])

    def replace_on_grid(arr2D, po_y, po_x, tg_y, tg_x):
        value_po = arr2D[po_y][po_x]
        value_tg = arr2D[tg_y][tg_x]
        arr2D[po_y][po_x] = value_tg
        arr2D[tg_y][tg_x] = value_po

    def check_corner(self, corner, points=False, distance=1, random=False):
        if random:
            corner_y = np.random.choice(['u', 'd', '.'], distance)[0]
            corner_x = np.random.choice(['r', 'l', '.'], distance)[0]
            corner = corner_y+corner_x

        ud = distance if corner[0] == 'u' else -distance
        rl = distance if corner[1] == 'r' else -distance
        if corner[0] == '.':
            ud = 0
        if corner[1] == '.':
            rl = 0

        if points:
            return {'y':  self.point_y + ud, 'x':  self.point_x + rl}
        try:
            value = self.arr2D[self.point_y + ud][self.point_x + rl]
        except:
            value = False
        return value

    @property
    def corners_condition(self, material) -> bool:
        return (self.check_corner('.l') == material or
                self.check_corner('.r') == material) and (self.check_corner('d.') == material or
                                                          self.check_corner('u.') == material)

    def find_value_grid(self, point_x, point_y, arr2D, value=None):
        self.arr2D = arr2D
        self.point_x = point_x
        self.point_y = point_y
        for material in config['types_to_group']:
            if self.check_corner('..') == material:
                check_number = {'repeat': 0, 'vector': 0}
                if self.corners_condition(material):
                    continue
                else:
                    for el in range(move_quality):
                        check_number['vector'] = 0
                        connections_edge_diagonally = []
                        for corner_vector in ['ul', 'ur', 'dl', 'dr']:
                            if self.check_corner(corner_vector) != material:
                                connections_edge_diagonally.append(
                                    corner_vector)

                        for corner_vector in connections_edge_diagonally:
                            for it in range(2, int(config['find_round'])):
                                if self.check_corner(corner_vector, distance=it) == material:
                                    check_number['vector'] = self.check_corner(
                                        corner_vector, distance=it-1, points=True)
                                    break

                            if check_number.get('vector') != 0:
                                pos = check_number.get('vector')
                                self.replace_on_grid(arr2D, point_y, point_x,
                                                     pos.get('y'), pos.get('x'))

                        connections_edge = []
                        for corner_vector in ['u.', '.r', 'd.', '.l']:
                            if self.check_corner(corner_vector) != material:
                                connections_edge.append(corner_vector)

                        for corner_vector in connections_edge:
                            for it in range(2, int(config['find_round'])):
                                if self.check_corner(corner_vector, distance=it) == material:
                                    check_number['vector'] = self.check_corner(
                                        corner_vector, distance=it-1, points=True)
                                    break

                            if check_number.get('vector') != 0:
                                pos = check_number.get('vector')
                                self.replace_on_grid(arr2D, point_y, point_x,
                                                     pos.get('y'), pos.get('x'))
                        else:
                            pass
                break
