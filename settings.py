import math

# canvas settigns
ARR_SIZE = 32
GENERATION_NUMBER = 0
PATH_MIXTURE = f"maps_gen/generations_{GENERATION_NUMBER}"
PATH_GENERATION = f"maps_gen/new_gener_{GENERATION_NUMBER}"
FILENAME = "map_gen"
NUMBER_FILES = 1

# render settings
QUALITY = 100
FIND_AROUND_RANGE = 4
MOVE_QUALITY = 20

# colors and types settings
DATA_COLOR_VALUE = {
    "void": "#ffffff",
    "grass": "#6abe30",
    "stone": "#696a6a",
    "hill": "#494949",
    "jungle": "#74a83c",
    "forest": "#57904c",
    "low_forest": "#7bc66e",
}
DEFAULT_COLOR = "#ffffff"
PROBABILITY = [0.35, 0.4, 0.05, 0.05, 0.05, 0.05, 0.05]
PATTERN_TYPES = ["void", "grass", "stone", "hill", "jungle", "forest", "low_forest"]
TYPES_TO_GROUP = ["void", "grass", "hill", "jungle", "forest"]
MIXTURE_QUALITY = 100
CORNER_TYPES = [
    "tl",  # top-left
    "tr",  # top-right
    "bl",  # bottom-left
    "br",  # bottom-right
    "t.",  # top
    ".r",  # right
    "b.",  # bottom
    ".l",  # left
]


# corners settings on mixture map
CORNER = math.ceil(ARR_SIZE / 3.3)
UP_CORNER_LIMIT = math.ceil(-(math.log(ARR_SIZE, 2) * 2) - 1)
HYPERBOLE = -2.2
POWER = -0.03
