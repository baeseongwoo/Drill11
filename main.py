from pico2d import *


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


running = True

open_canvas()
# game loop
while running:
    handle_events()
    clear_canvas()
    update_canvas()
    delay(0.01)
# finalization code
close_canvas()
