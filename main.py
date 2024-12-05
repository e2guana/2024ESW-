from Joystick import Joystick
from game import AstroEvasion
from PIL import Image, ImageDraw, ImageFont
import time

def read_buttons(joystick):
    return {
        "up": not joystick.button_U.value,
        "down": not joystick.button_D.value,
        "left": not joystick.button_L.value,
        "right": not joystick.button_R.value,
        "fire": not joystick.button_A.value,
        "barrier": not joystick.button_B.value,
    }
    
def show_logo_screen(joystick):
    # 시작화면 로딩
    logo = Image.open("assets/AstroEvasion.png")
    logo = logo.resize((joystick.width, joystick.height))
    joystick.disp.image(logo)

    print("Press A or B to start the game.")

    # 버튼 입력 대기
    while True:
        buttons = read_buttons(joystick)
        if buttons["fire"] or buttons["barrier"]:  # A or B 버튼 누르면 시작
            return
        time.sleep(0.1)

def show_game_over_screen(joystick, score):
    # 게임오버 화면
    game_over_image = Image.open("assets/GameOver.png")
    game_over_image = game_over_image.resize((joystick.width, joystick.height))
    draw = ImageDraw.Draw(game_over_image)
    
    # 기본 폰트 설정
    font = ImageFont.load_default()
    
    # 점수 표시
    score_text = f"Final Score: {score}"
    score_bbox = draw.textbbox((0, 0), score_text, font=font)  # 텍스트 경계 계산
    score_width = score_bbox[2] - score_bbox[0]
    text_x = (joystick.width - score_width) // 2
    score_y = joystick.height // 2 + 50
    draw.text((text_x, score_y), score_text, fill=(255, 255, 255), font=font)

    # 안내 메시지 표시
    message_text = "Press any button to restart"
    message_bbox = draw.textbbox((0, 0), message_text, font=font)  # 텍스트 경계 계산
    message_width = message_bbox[2] - message_bbox[0]
    message_x = (joystick.width - message_width) // 2
    message_y = score_y + 30
    draw.text((message_x, message_y), message_text, fill=(255, 255, 255), font=font)
    
    joystick.disp.image(game_over_image)
    
    while True:
        buttons = read_buttons(joystick)
        if buttons["fire"] or buttons["barrier"]:  # A or B 버튼 누르면 재시작
            return
        time.sleep(0.1)


def main():
    joystick = Joystick()

    # 게임 루프
    while True: 
        # 로고 화면 표시
        show_logo_screen(joystick)

        # 게임 시작
        game = AstroEvasion(joystick)
        while not game.game_over:
            buttons = read_buttons(joystick)
            game.update(buttons)
            game.add_obstacle()
            game.draw()
            joystick.disp.image(game.image)
            time.sleep(0.05)

        # 게임 오버 화면 표시 및 재시작 대기
        show_game_over_screen(joystick, game.score)

if __name__ == "__main__":
    main()
