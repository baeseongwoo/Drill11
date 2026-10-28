from pico2d import *

import game_world
from grass import Grass  # grass는 모듈 이름, Grass는 그 안의 클래스


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    game_world.world.clear()

    grass = Grass()
    game_world.add_object(grass)


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    game_world.update()
    clear_canvas()
    game_world.render()
    update_canvas()
    delay(0.01)
# finalization code
close_canvas()
