# Drill11 - 캐릭터 컨트롤러 (클래스와 모듈)

잔디 위의 소년을 좌우 방향키로 달리게 하는 pico2d 프로그램. 요구사항과 설계는 [PRD.md](PRD.md), 상태 다이어그램은 [state_diagram.png](state_diagram.png) 참고.

## 실행

```
pip install -r requirements.txt
python main.py
```

VS Code: 이 폴더(Drill11)를 열고 **Ctrl+F5**.

## 조작

| 키 | 동작 |
|---|---|
| ← / → | 달리기 (벽에 닿으면 그 자리에서 멈춤), 떼면 서 있기 |
| a | 서 있을 때 누르면 자동 무적 런: 2배 속도·2배 크기로 혼자 좌우 왕복, 5초 뒤 서 있기로 돌아감. 도중에 ← / →를 누르면 그 방향으로 달리기 |
| ESC | 종료 |

## 파일

| 파일 | 내용 |
|---|---|
| `main.py` | 게임 루프 |
| `game_world.py` | 게임 객체 목록 모듈 |
| `state_machine.py` | `StateMachine` 클래스 |
| `boy.py` | `Idle`, `Run`, `AutoRun` 상태 클래스와 `Boy` 클래스 |
| `grass.py` | `Grass` 클래스 |
| `animation_sheet.png`, `grass.png` | 이미지 리소스 |
| `state_diagram.png` | 상태 다이어그램 |
