import math

# canvas settigns
arr_size = 32
generation_number = 0
path_mixture = f"maps_gen/generations_{generation_number}"
path_generation = f"maps_gen/new_gener_{generation_number}"
filename = "map_gen"
number_files = 1

# render settings
quality = 350
find_round = 20
move_quality = 40

# colors and types settings
data_color_value = {
    "void": "#ffffff",
    "grass": "#6abe30",
    "stone": "#696a6a",
    "hill": "#494949",
    "jungle": "#74a83c",
    "forest": "#57904c",
    "low_forest": "#7bc66e",
}
probability = [0.35, 0.4, 0.05, 0.05, 0.05, 0.05, 0.05]
pattern_types = ["void", "grass", "stone", "hill", "jungle", "forest", "low_forest"]
types_to_group = ["void", "grass", "hill", "jungle", "forest"]
mixture_quality = 100

# corners settings on mixture map
corner = math.ceil(arr_size / 3.3)
corner_ = corner
up_corner_limit = math.ceil(-(math.log(arr_size, 2) * 2) - 1)
hyperbole = -2.1
power = -0.03
