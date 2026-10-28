from pico2d import load_image, get_time, get_canvas_width, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_a

from state_machine import StateMachine

RUN_SPEED = 300  # 달리기 속도 (px/초)
HALF_WIDTH = 50  # 소년 칸 폭의 절반 (화면 밖으로 안 나가게 할 때 사용)
IDLE_FPS = 8     # 서 있기 애니메이션: 초당 8장
RUN_FPS = 12     # 달리기 애니메이션: 초당 12장
MAX_FRAME_TIME = 0.1  # 창을 끄는 등 루프가 멈췄다 돌아와도 한 번에 크게 건너뛰지 않게
AUTO_RUN_SPEED = RUN_SPEED * 2  # 자동 무적 런 속도: 달리기의 2배
AUTO_RUN_SCALE = 2               # 자동 무적 런 크기: 2배
AUTO_RUN_TIME = 5.0              # 자동 무적 런 지속 시간(초)


# 상태 이벤트 검사 함수: 상태 이벤트는 ('DIR', dir) 모양의 튜플
def dir_on(e):
    return e[0] == 'DIR' and e[1] != 0  # ← 또는 → 하나만 눌려 있음


def dir_off(e):
    return e[0] == 'DIR' and e[1] == 0  # 키를 모두 뗐거나 양쪽을 함께 누름


def a_down(e):
    return e[0] == 'A_DOWN'  # 'a' 키를 누름


def time_out(e):
    return e[0] == 'TIME_OUT'  # 자동 무적 런 시간이 끝남


class Idle:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = 0

    def exit(self, e):
        pass

    def do(self, frame_time):
        self.boy.frame = (self.boy.frame + IDLE_FPS * frame_time) % 8

    def draw(self):
        boy = self.boy
        if boy.face_dir == 1:
            boy.image.clip_draw(int(boy.frame) * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame) * 100, 200, 100, 100, boy.x, boy.y)


class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = e[1]  # 이벤트에 담긴 방향으로 달린다
        self.boy.face_dir = e[1]

    def exit(self, e):
        pass

    def do(self, frame_time):
        self.boy.frame = (self.boy.frame + RUN_FPS * frame_time) % 8
        self.boy.x += self.boy.dir * RUN_SPEED * frame_time
        self.boy.x = max(HALF_WIDTH, min(self.boy.x, get_canvas_width() - HALF_WIDTH))  # 벽에서는 멈춘다

    def draw(self):
        boy = self.boy
        if boy.face_dir == 1:  # 오른쪽 달리기 줄 100, 왼쪽 달리기 줄 0
            boy.image.clip_draw(int(boy.frame) * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, boy.y)


class AutoRun:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dir = self.boy.face_dir  # 바라보던 방향으로 자동으로 달리기 시작
        self.start_time = get_time()

    def exit(self, e):
        pass

    def do(self, frame_time):
        boy = self.boy
        boy.frame = (boy.frame + RUN_FPS * frame_time) % 8
        boy.x += boy.dir * AUTO_RUN_SPEED * frame_time

        # 커진 크기만큼 벽 기준을 넓혀서, 벽에 닿으면 반대 방향으로 전환
        half_width = HALF_WIDTH * AUTO_RUN_SCALE
        boy.x = max(half_width, min(boy.x, get_canvas_width() - half_width))
        if (boy.x <= half_width and boy.dir == -1) or                 (boy.x >= get_canvas_width() - half_width and boy.dir == 1):
            boy.dir = -boy.dir
            boy.face_dir = boy.dir

        if get_time() - self.start_time >= AUTO_RUN_TIME:
            boy.state_machine.handle_state_event(('TIME_OUT', 0))

    def draw(self):
        boy = self.boy
        size = 100 * AUTO_RUN_SCALE
        y = boy.y + (size - 100) // 2  # 커져도 발이 잔디 위에 붙어 있게 위로 올림
        if boy.face_dir == 1:
            boy.image.clip_draw(int(boy.frame) * 100, 100, 100, 100, boy.x, y, size, size)
        else:
            boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, boy.x, y, size, size)


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
        self.last_update_time = get_time()

        # 상태 객체를 만들고, 상태 머신은 IDLE에서 시작
        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.AUTO_RUN = AutoRun(self)
        self.state_machine = StateMachine(self.IDLE, {
            self.IDLE: {dir_on: self.RUN, a_down: self.AUTO_RUN},
            self.RUN: {dir_off: self.IDLE},
            self.AUTO_RUN: {time_out: self.IDLE, dir_on: self.RUN},
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            self.state_machine.handle_state_event(('A_DOWN', 0))

    def update(self):
        now = get_time()
        frame_time = min(now - self.last_update_time, MAX_FRAME_TIME)  # 지난 프레임부터 흐른 시간(초)
        self.last_update_time = now
        self.state_machine.update(frame_time)

    def draw(self):
        self.state_machine.draw()
