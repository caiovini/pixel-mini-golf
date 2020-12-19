import pygame as pg
import pymunk as pm

import sys

from assets import Background, Tile, fetch_tile_map, Flag
from physics import Ball, Stick, post_solve_stick_ball, post_solve_segment_ball
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from functools import wraps
from collections import deque
from os.path import join

WHITE = pg.Color(255, 255, 255)
BLACK = pg.Color(0, 0, 0)
YELLOW = pg.Color(255, 255, 0)

clock = pg.time.Clock()
step_space = 1/60

ball_radius = 0xA
stick_radius = 0xF


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Pixel minigolf")

    space = pm.Space()
    space.gravity = (0.0, 500.0)  # Define initial gravity

    ball = Ball(position=(200, 200), collision_type=1,
                radius=ball_radius, mass=1)
    stick = Stick(position=(0, 0), collision_type=2,
                  radius=stick_radius, mass=10)
    tile = Tile()
    flag = Flag()
    tiles = fetch_tile_map()
    tiles_ = deque(tiles)

    font = pg.font.Font(join("fonts", "segoe-ui-symbol.ttf"), 20)

    pm.Segment.elasticity = 0.5

    def build_static_lines_tile(func) -> object:

        @wraps(func)
        def build():
            """
                Build segments where collisions will happen to the ball
                This is executed while deque of balls is greater than zero
                After that the while loop won't be executed anymore and func will be called

            """

            while len(tiles_) > 0:

                body = pm.Body(body_type=pm.Body.STATIC)
                space.add(body)

                t = tiles_.pop()
                tile.set_image(t["type"])
                tile.set_position(t["x"], t["y"])
                seg = pm.Segment(body, (tile.rect.x, tile.rect.y),
                                 (tile.rect.x + tile.image.get_rect().size[0], tile.rect.y), 1)
                seg.collision_type = 3
                space.add(seg)

            func()

        return build

    @build_static_lines_tile
    def build_tiles():

        for t in tiles:
            tile.set_image(t["type"])
            tile.set_position(t["x"], t["y"])
            screen.blit(tile.image, tile.rect)

    background = Background()

    alpha_bg = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    alpha_bg.set_alpha(50)
    alpha_bg.fill((BLACK))

    def create_static_lines() -> list:

        body = pm.Body(body_type=pm.Body.STATIC)

        segment_1 = pm.Segment(body, (0, 0), (SCREEN_WIDTH, 0), 15)
        segment_2 = pm.Segment(body, (0, 0), (0, SCREEN_HEIGHT), 15)
        segment_3 = pm.Segment(body, (SCREEN_WIDTH, 0),
                               (SCREEN_WIDTH, SCREEN_HEIGHT), 15)

        return[body, segment_1, segment_2, segment_3]

    flag.set_position(900, 340)

    space.add(*create_static_lines())
    space.add(ball.body, ball.shape)
    space.add(stick.body, stick.shape)

    space.add_collision_handler(1, 2).post_solve = post_solve_stick_ball
    space.add_collision_handler(1, 3).post_solve = post_solve_segment_ball

    mouse_x, mouse_y = 0, 0
    game_win = game_over = done = False
    while not done:

        screen.blit(background.image, background.rect)

        screen.blit(flag.image, flag.rect)
        screen.blit(alpha_bg, (0, 0))
        build_tiles()

        pg.draw.circle(
            screen, WHITE, ball.body.position, ball_radius, width=0)

        pg.draw.circle(
            screen, WHITE, (mouse_x, mouse_y), stick_radius, width=0)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                done = True

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    done = True

            if event.type == pg.MOUSEMOTION:

                mouse_x, mouse_y = event.pos

                if not game_over and not game_win:
                    stick.set_position(mouse_x, mouse_y)

                else:
                    stick.set_position(0, 0)  # Don't hit the ball

        if ball.body.position.y > 465:
            game_over = True

        if flag.rect.colliderect(pg.Rect(ball.body.position.x,
                                         ball.body.position.y,
                                         ball_radius, ball_radius)) \
           and not game_over:

            alpha_bg.set_alpha(128)
            screen.blit(alpha_bg, (0, 0))
            label = font.render("Victory !!!", 1, YELLOW)
            screen.blit(label, (SCREEN_WIDTH / 2.2, SCREEN_HEIGHT / 2.5))
            game_win = True

            if ball.shape in space.shapes:
                space.remove(ball.shape, ball.body)

        if game_over and not game_win:
            alpha_bg.set_alpha(128)
            screen.blit(alpha_bg, (0, 0))
            label = font.render("GAME OVER !!!", 1, YELLOW)
            screen.blit(label, (SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2.5))

        space.step(step_space)
        pg.display.flip()
        clock.tick(30)  # FPS


if __name__ == "__main__":
    sys.exit(main())
