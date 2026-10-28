# 게임 월드 모듈: import 하면 모듈 자체가 하나뿐인 객체(싱글톤)처럼 쓰인다

world = []  # 게임 객체들을 담는 리스트


def add_object(o):
    world.append(o)
