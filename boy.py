from pico2d import load_image

from state_machine import StateMachine


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


class Boy:
    image = None  # 클래스 변수: 소년이 여러 명이어도 시트는 한 번만 로드

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1  # 바라보는 방향: 1 오른쪽, -1 왼쪽
        self.dir = 0       # 이동 방향: 1 오른쪽, -1 왼쪽, 0 정지
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')

        # 상태 객체를 만들고, 상태 머신은 IDLE에서 시작
        self.IDLE = Idle(self)
        self.state_machine = StateMachine(self.IDLE)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
