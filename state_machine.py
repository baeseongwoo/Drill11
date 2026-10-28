# 상태 머신 모듈: 상태 객체는 enter(e), exit(e), do(), draw() 를 가지고 있어야 한다


class StateMachine:
    def __init__(self, start_state):
        self.cur_state = start_state
        self.cur_state.enter(('START', 0))

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()
