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
| ← / → | 달리기 (벽에 닿으면 바로 반대 방향으로 돌아섬), 떼면 멈춤 |
| ESC | 종료 |

## 파일

| 파일 | 내용 |
|---|---|
| `main.py` | 게임 루프 |
| `game_world.py` | 게임 객체 목록 모듈 |
| `state_machine.py` | `StateMachine` 클래스 |
| `boy.py` | `Idle`, `Run` 상태 클래스와 `Boy` 클래스 |
| `grass.py` | `Grass` 클래스 |
| `animation_sheet.png`, `grass.png` | 이미지 리소스 |
| `state_diagram.png` | 상태 다이어그램 |
