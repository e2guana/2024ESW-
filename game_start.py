from Joystick import *
from PIL import Image, ImageDraw, ImageFont
from src.game_start import GameStart
from src.Button import Button

class GameStart:
    def __init__(self):
        joystick = Joystick()
         
        self.__width = joystick.width
        self.__height = joystick.height
        self.__image = Image.open("assets/AstroEvasion.png").convert("RGB").resize((self.__width, self.__height))
        self.__draw = ImageDraw.Draw(self.__image)
        self.__fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        self.__level = 1

    def __call__(self):
        button = Button()

        while True:
            # AstroEvasion 화면 출력
            DISPLAY.image(self.__image)

            # 버튼 입력 처리
            if button.b:  # B 버튼을 누르면 게임 시작
                self.gameStart(self.__level)
                break

    def gameStart(self, level):
        game_start = GameStart(level, Background('background'))
        game_start()
