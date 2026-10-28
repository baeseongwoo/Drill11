from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT

from state_machine import StateMachine


# 상태 이벤트 검사 함수: 상태 이벤트는 ('DIR', dir) 모양의 튜플
def dir_on(e):
    return e[0] == 'DIR' and e[1] != 0  # ← 또는 → 하나만 눌려 있음


def dir_off(e):
    return e[0] == 'DIR' and e[1] == 0  # 키를 모두 뗐거나 양쪽을 함께 누름


class Idle:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        boy = self.boy
        if boy.face_dir == 1:
            boy.image.clip_draw(boy.frame * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 200, 100, 100, boy.x, boy.y)


class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = e[1]  # 이벤트에 담긴 방향으로 달린다
        self.boy.face_dir = e[1]

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x += self.boy.dir * 5

    def draw(self):
        boy = self.boy
        boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)


class Boy:
    image = None  # 클래스 변수: 소년이 여러 명이어도 시트는 한 번만 로드

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1  # 바라보는 방향: 1 오른쪽, -1 왼쪽
        self.dir = 0       # 이동 방향: 1 오른쪽, -1 왼쪽, 0 정지
        self.left_pressed = False
        self.right_pressed = False
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')

        # 상태 객체를 만들고, 상태 머신은 IDLE에서 시작
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(self.IDLE, {
            self.IDLE: {dir_on: self.RUN},
            self.RUN: {dir_off: self.IDLE},
        })

    # 키 입력을 방향으로 바꿔 상태 머신에 ('DIR', dir) 이벤트로 넘긴다
    def handle_event(self, event):
        if event.type in (SDL_KEYDOWN, SDL_KEYUP) and event.key in (SDLK_LEFT, SDLK_RIGHT):
            pressed = event.type == SDL_KEYDOWN
            if event.key == SDLK_LEFT:
                self.left_pressed = pressed
            else:
                self.right_pressed = pressed

            key_dir = int(self.right_pressed) - int(self.left_pressed)  # 둘 다 눌리면 0
            self.state_machine.handle_state_event(('DIR', key_dir))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
