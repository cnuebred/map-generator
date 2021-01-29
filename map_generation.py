import os
from map_mixture import generate
import subprocess
import multitasking
import sys
import json
from PIL import Image, ImageDraw
import numpy as np
from numpy.core.fromnumeric import repeat


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
# ==
get_data_base_by_color = config["get_data_base_by_color"]
get_data_base_by_type = config["get_data_base_by_type"]
# ==

arr_size_x, arr_size_y = config["arr_size"], config["arr_size"]

array_ = np.full((arr_size_x, arr_size_y), "...............")


def get_value_by_color(arg):
    target = '#{:02x}{:02x}{:02x}'.format(arg[0], arg[1], arg[2])
    return get_data_base_by_color.get(target, None)


def getcolor(c):
    return get_data_base_by_type.get(c, '#ffffff')


def replace_on_grid(arr2D, po_y, po_x, tg_y, tg_x):
    value_po = arr2D[po_y][po_x]
    value_tg = arr2D[tg_y][tg_x]
    arr2D[po_y][po_x] = value_tg
    arr2D[tg_y][tg_x] = value_po


def find_value_grid(point_x, point_y, arr2D, value=None):
    def check_corner(corner, points=False, distance=1, random=False):
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
            return {'y': point_y + ud, 'x': point_x + rl}
        try:
            value = arr2D[point_y + ud][point_x + rl]
        except:
            value = False
        return value

    for material in config['types_to_group']:
        if check_corner('..') == material:
            check_number = {'repeat': 0, 'vector': 0}
            if (check_corner('.l') == material or check_corner('.r') == material) and (check_corner('d.') == material or check_corner('u.') == material):
                continue
            else:
                for el in range(move_quality):
                    check_number['vector'] = 0
                    connections_edge_diagonally = []
                    for corner_vector in ['ul', 'ur', 'dl', 'dr']:
                        if check_corner(corner_vector) != material:
                            connections_edge_diagonally.append(corner_vector)

                    for corner_vector in connections_edge_diagonally:
                        for it in range(2, int(config['find_round'])):
                            if check_corner(corner_vector, distance=it) == material:
                                check_number['vector'] = check_corner(
                                    corner_vector, distance=it-1, points=True)
                                break

                        if check_number.get('vector') != 0:
                            pos = check_number.get('vector')
                            replace_on_grid(arr2D, point_y, point_x,
                                            pos.get('y'), pos.get('x'))

                    connections_edge = []
                    for corner_vector in ['u.', '.r', 'd.', '.l']:
                        if check_corner(corner_vector) != material:
                            connections_edge.append(corner_vector)

                    for corner_vector in connections_edge:
                        for it in range(2, int(config['find_round'])):
                            if check_corner(corner_vector, distance=it) == material:
                                check_number['vector'] = check_corner(
                                    corner_vector, distance=it-1, points=True)
                                break

                        if check_number.get('vector') != 0:
                            pos = check_number.get('vector')
                            replace_on_grid(arr2D, point_y, point_x,
                                            pos.get('y'), pos.get('x'))
                    else:
                        pass
            break


def create_pixel_map(pix):
    for y in range(arr_size_y):
        for x in range(arr_size_x):
            array_[y][x] = get_value_by_color(pix[x, y])
    return array_


def save_as_image(path, arr):
    im = Image.new('RGBA', (arr_size_x, arr_size_y), (20, 255, 0, 0))
    draw = ImageDraw.Draw(im)
    for dx in range(arr_size_x):
        for dy in range(arr_size_y):
            draw.line((dx, dy, dx, dy), fill=getcolor(arr[dy][dx]))

    # ig = Image.open(BytesIO(im))       ## generates to buffor
    # buffor = BytesIO()        ## generates to buffor
    print('image generated')
    im.save(path, 'PNG')  # generates to buffor - replace path <-> buffor
    # buffor.seek(0)    ## if generates to buffor


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


for file_number in range(0, number_files):
    # im = Image.open(f'{path_generation}/map_generation_r{file}.png')   ## generates from the image
    pix = generate()  # generates from the buffor
    array_ = create_pixel_map(pix)
    for x in progressbar(range(quality), f"Quality progress - image {file_number}: ", 40):
        for y in range(arr_size_y):
            for idx, x in enumerate(array_[y]):
                find_value_grid(idx, y, array_, x)

    if not os.path.exists(path_new_generation):
        os.makedirs(path_new_generation)
    save_as_image(
        f'{path_new_generation}/{filename}_{file_number}.png', array_)


# subprocess.run(['python', 'map_mixture.py',
#                 f'{gen + 1}'], capture_output=False)

# ^ code to separate basic image and new generation from image
