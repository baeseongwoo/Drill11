# 상태 머신 모듈: 상태 객체는 enter(e), exit(e), do(frame_time), draw() 를 가지고 있어야 한다


class StateMachine:
    # rules: {현재 상태: {이벤트 검사 함수: 다음 상태}}
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter(('START', 0))

    # 상태 이벤트가 들어오면 현재 상태의 규칙을 차례로 검사해 맞는 것이 있으면 전이
    def handle_state_event(self, state_event):
        for check_event, next_state in self.rules[self.cur_state].items():
            if check_event(state_event):
                self.cur_state.exit(state_event)
                self.cur_state = next_state
                self.cur_state.enter(state_event)
                return

    def update(self, frame_time):
        self.cur_state.do(frame_time)

    def draw(self):
        self.cur_state.draw()
