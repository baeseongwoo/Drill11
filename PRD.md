# PRD - Drill #11 클래스와 모듈로 만드는 캐릭터 컨트롤러

## 1. 개요

LEC12(캐릭터 컨트롤러 1)의 **클래스 변수**, **모듈과 소스 코드 분리**, **상태 머신**을 적용해, 잔디 위의 소년을 좌우 방향키로 달리게 하는 pico2d 프로그램을 만든다. 게임 객체(소년, 잔디)와 상태(IDLE, RUN), 상태 머신, 게임 월드를 각각 **클래스와 모듈**로 나눈다.

| 항목 | 내용 |
|---|---|
| 소스 | `main.py`, `game_world.py`, `state_machine.py`, `boy.py`, `grass.py` |
| 리소스 | `animation_sheet.png` (소년), `grass.png` (잔디) |
| 상태 다이어그램 | `state_diagram.png` |
| 라이브러리 | pico2d (`pip install -r requirements.txt`) |
| 실행 | 저장소 폴더에서 `python main.py`, 또는 VS Code로 이 폴더를 열고 Ctrl+F5 |
| 저장소 | https://github.com/baeseongwoo/Drill11.git |

## 2. 요구사항

| ID | 요구사항 | 구현 기준 |
|---|---|---|
| R1 | 모듈 분리 | 역할별로 파일을 나누고 `import`해서 사용 (4절) |
| R2 | 클래스로 구현 | 게임 객체(`Boy`, `Grass`), 상태(`Idle`, `Run`), 상태 머신(`StateMachine`)을 모두 클래스로 만든다 |
| R3 | 리소스 로딩 최적화 | 이미지는 클래스 변수 `image`에 한 번만 로드하고 모든 객체가 공유 |
| R4 | 상태 머신 | IDLE / RUN 두 상태. 상태 전이는 `StateMachine`의 규칙 테이블로 처리 |
| R5 | IDLE | 처음 상태. 바라보는 방향의 서 있기 애니메이션 반복 |
| R6 | RUN | ←/→를 누르면 RUN으로 그 방향 달리기, 모두 떼면 IDLE. 좌우를 하나의 RUN 상태로 처리 |
| R7 | 벽에서 방향 전환 | 화면 좌우 밖으로 나가지 않고, 벽에 닿는 그 프레임에 바로 반대 방향으로 돌아서 계속 달림 |
| R8 | 종료 | ESC 또는 창 닫기 |
| R9 | 커밋 로그 | 한 커밋에 한 가지 변경, 모든 커밋은 실행 가능한 상태, 25개 이상 (7절) |
| R10 | 상태 다이어그램 | 구현한 상태와 전이를 그림으로 만들어 저장소에 포함 |

범위 밖: SLEEP(잠들기), Dash, 위아래 이동, 충돌 처리.

## 3. 리소스

### 3.1 animation_sheet.png (802 x 402)

100 x 100 칸이 가로 8개(프레임), 세로 4줄(동작). pico2d 기준(이미지 아래쪽에서부터) 줄 위치:

| bottom | 동작 |
|---|---|
| 300 | 오른쪽을 보고 서 있기 (IDLE) |
| 200 | 왼쪽을 보고 서 있기 (IDLE) |
| 100 | 오른쪽으로 달리기 (RUN) |
| 0 | 왼쪽으로 달리기 (RUN) |

### 3.2 grass.png

캔버스 기본 크기(800 x 600) 폭의 잔디. `(400, 30)`에 그린다. 소년은 그 위 `y = 90`에 선다.

## 4. 모듈 구조

| 모듈 | 클래스 / 함수 | 역할 |
|---|---|---|
| `main.py` | `handle_events()`, `reset_world()` | 게임 루프. 종료 이벤트 처리, 나머지 이벤트는 소년에게 전달 |
| `game_world.py` | `world`, `add_object()`, `update()`, `render()` | 게임 객체 목록. 모듈 자체가 하나뿐인 객체(싱글톤)로 쓰인다 |
| `state_machine.py` | `StateMachine` | 현재 상태를 들고, 규칙 테이블에 따라 상태를 바꾸고, `update`/`draw`를 현재 상태에 맡김 |
| `boy.py` | `Idle`, `Run`, `Boy` | 상태 클래스와 소년. 소년은 상태 머신을 하나 가진다 |
| `grass.py` | `Grass` | 잔디 |

```
main.py ──import──▶ game_world.py
   │                    ▲ add_object(grass), add_object(boy)
   ├──import──▶ grass.py   class Grass
   └──import──▶ boy.py     class Idle, Run, Boy ──import──▶ state_machine.py  class StateMachine
```

- 모든 게임 객체는 `update()`와 `draw()`를 가진다. `game_world`는 객체 종류를 모르고 두 메서드만 호출한다.
- 모든 상태 클래스는 `enter(e)`, `exit(e)`, `do(frame_time)`, `draw()`를 가진다. `StateMachine`은 상태 종류를 모르고 이 네 메서드만 호출한다.

## 5. 상태 머신

![상태 다이어그램](state_diagram.png)

### 5.1 상태 이벤트

키 입력을 그대로 상태 머신에 넘기지 않고, 소년이 먼저 **방향(dir)** 으로 바꿔 `('DIR', dir)` 이벤트를 만든다.

- `dir = int(right_pressed) - int(left_pressed)` : 1 오른쪽, -1 왼쪽, 0 정지 (두 키를 함께 누르면 0)
- `dir_on(e)` : `dir != 0` / `dir_off(e)` : `dir == 0`

### 5.2 규칙 테이블

| 현재 상태 | 이벤트 | 다음 상태 |
|---|---|---|
| IDLE | `dir_on` (←/→ 누름) | RUN |
| RUN | `dir_off` (키를 모두 뗌, 또는 양쪽 동시) | IDLE |

### 5.3 상태별 동작

| 상태 | enter | do | draw |
|---|---|---|---|
| IDLE | `dir = 0` | 프레임 진행 (`IDLE_FPS`) | 바라보는 방향의 서 있기 줄 |
| RUN | `dir`, `face_dir`를 이벤트의 방향으로 | 프레임 진행 (`RUN_FPS`), `dir` 방향으로 이동, 경계 제한, 벽에 닿으면 `dir`·`face_dir` 반전 | 바라보는 방향의 달리기 줄 |

- 벽 반전은 상태가 바뀌는 것이 아니라 RUN 안에서 방향만 바뀐다 (다이어그램의 RUN 자기 전이).
- 벽에서 돌아선 뒤에도 키를 누르고 있는 동안은 계속 달리고(양쪽 벽 사이 왕복), 키를 떼면 IDLE이 된다.

## 6. 상수 (`boy.py`)

| 상수 | 값 | 의미 |
|---|---|---|
| `RUN_SPEED` | 300 | 달리기 속도 (px/초) |
| `HALF_WIDTH` | 50 | 소년 칸의 반폭. x는 50 ~ 750으로 제한 |
| `IDLE_FPS` / `RUN_FPS` | 8 / 12 | 애니메이션 속도 (프레임/초) |
| `MAX_FRAME_TIME` | 0.1 | 루프가 잠깐 멈췄다 돌아와도 한 번에 크게 건너뛰지 않도록 한 프레임 시간의 상한 |

## 7. 개발 단계와 커밋

규칙: 커밋 메시지는 한글. 한 커밋에 한 가지 변경. 모든 커밋은 실행 가능한 상태.

| 단계 | # | 커밋 |
|---|---|---|
| 준비 | 1 | 리포지토리 환경 셋팅 |
| | 2 | 이미지 리소스 추가 |
| | 3 | PRD.md 작성 |
| | 4 | 상태 다이어그램 추가 |
| 게임 루프 | 5 | `main.py` 게임 루프 뼈대 (창 닫기로 종료) |
| | 6 | ESC로 종료 |
| 게임 월드 모듈 | 7 | `game_world.py`: world 리스트와 `add_object()` |
| | 8 | `game_world.update()` / `render()`를 게임 루프에서 사용 |
| 잔디 | 9 | `grass.py`: Grass 클래스 |
| | 10 | Grass 이미지를 클래스 변수로 |
| 소년 | 11 | `boy.py`: Boy 클래스 (정지 그림) |
| | 12 | Boy 이미지를 클래스 변수로 |
| | 13 | 서 있기 애니메이션 |
| 상태 머신 | 14 | `state_machine.py`: StateMachine 클래스 |
| | 15 | Idle 상태 클래스, Boy가 상태 머신 사용 |
| | 16 | 종료 외 이벤트를 소년에게 전달 |
| | 17 | 방향키로 dir 계산 |
| | 18 | 상태 이벤트와 규칙 테이블로 전이 처리 |
| RUN | 19 | Run 상태 클래스와 IDLE → RUN 전이 |
| | 20 | RUN → IDLE 전이 |
| | 21 | 달리는 방향에 맞는 그림 |
| 다듬기 | 22 | 이동과 애니메이션을 시간 기반으로 |
| | 23 | 한 프레임 시간 상한 |
| | 24 | 화면 밖으로 나가지 않게 |
| | 25 | 벽에 닿자마자 반대 방향으로 전환 |
| 정리 | 26 | `requirements.txt` |
| | 27 | VS Code 실행 설정 |
| | 28 | README.md |
| | 29 | PRD.md에 검증 결과 반영 |

## 8. 검증 방법

`get_events()`를 가짜 키 입력으로 바꾼 스크립트로 `main.py`를 실행해 소년의 상태와 좌표를 확인한다 (스크립트는 저장소에 넣지 않는다). 각 커밋도 같은 스크립트로 오류 없이 실행·종료되는지 확인한 뒤 커밋한다.
