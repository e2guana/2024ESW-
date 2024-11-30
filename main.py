import time
from Joystick import Joystick
from display import Display

def main():
    # 조이스틱 및 디스플레이 초기화
    joystick = Joystick()
    display = Display()

    # 이미지 경로 설정
    start_screen_path = "assets/Start.png"  # 시작 화면 이미지
    game_screen_path = "assets/Background.png"  # 게임 화면 이미지

    # 시작 화면 출력
    display.display_image(start_screen_path)
    print("시작 화면 출력 중...")

    # 버튼 입력 대기
    while True:
        if joystick.any_button_pressed():
            print("버튼이 눌렸습니다! 게임 화면으로 전환합니다.")
            display.display_image(game_screen_path)  # 게임 화면 출력
            break
        time.sleep(0.1)

if __name__ == "__main__":
    main()
