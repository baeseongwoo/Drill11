from pico2d import load_image


class Boy:
    image = None  # 클래스 변수: 소년이 여러 명이어도 시트는 한 번만 로드

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1  # 바라보는 방향: 1 오른쪽, -1 왼쪽
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')

    def update(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
