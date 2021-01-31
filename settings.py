import math

# canvas settigns
arr_size = 32
gen = 0
path_mixture = f"maps_gen/generations_{gen}"
path_generation = f"maps_gen/new_gener_{gen}"
filename = "map_gen"
number_files = 1

# render settings
quality = 150
find_round = 5
move_quality = 100

# colors and types settings
data_color_value = {
    "#ffffff": "void",
    "#6abe30": "grass",
    "#696a6a": "stone",
    "#494949": "hill",
    "#74a83c": "jungle",
    "#57904c": "forest",
    "#7bc66e": "low_forest",
    "void": "#ffffff",
    "grass": "#6abe30",
    "stone": "#696a6a",
    "hill": "#494949",
    "jungle": "#74a83c",
    "forest": "#57904c",
    "low_forest": "#7bc66e",
}
probability = [0.55, 0.2, 0.05, 0.05, 0.05, 0.05, 0.05]
pattern_types = ["void", "grass", "stone", "hill", "jungle", "forest", "low_forest"]
types_to_group = ["void", "grass", "hill", "jungle", "forest"]
mixture_quality = 100

# corners settings on mixture map
corner = math.ceil(arr_size / 3.3)
corner_ = corner
up_corner_limit = math.ceil(-(math.log(arr_size, 2) * 2) - 1)
hyper_bol = -2.1
power = -0.03
