from pico2d import load_image


class Grass:
    image = None  # 클래스 변수: 모든 Grass 객체가 이미지 하나를 공유

    def __init__(self):
        if Grass.image == None:  # 처음 만들 때만 로드
            Grass.image = load_image('grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
