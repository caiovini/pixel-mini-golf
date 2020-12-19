import pygame as pg


from json import loads
from os.path import join
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

_background_path = join("assets", "png", "BG", "BG.png")
_tiles = join("assets", "png", "Tiles")
_map1 = join("assets", "map1.json")
_flag = join("assets", "png", "Object", "flag.png")


_tile_scale = (60, 60)
_flag_scale = (60, 60)


class Base(pg.sprite.Sprite):

    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

    def set_position(self, x, y) -> None:

        # Change my rectangle

        self.rect.x = x
        self.rect.y = y


class Background(Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(_background_path)
                                   .convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        Base.__init__(self, image)


class Flag(Base):

    def __init__(self):
        image = pg.transform.scale(pg.image.load(_flag)
                                   .convert_alpha(), _flag_scale)
        Base.__init__(self, image)


class Tile(Base):

    def __init__(self):
        self.images = {i: pg.transform.scale(pg.image.load(join(_tiles, str(i) + ".png"))
                                             .convert_alpha(), _tile_scale) for i in range(1, 19)}

        image = self.images[1]  # Init
        Base.__init__(self, image)

    def set_image(self, ind: int):
        self.image = self.images[ind]


def fetch_tile_map():

    with open(_map1, "r") as myfile:  # Open json file
        data = myfile.read()
        tiles = loads(data)

    return tiles
