from game_object import ObjectController
from game_situation import GameSituation
from PIL import Image, ImageDraw, ImageFont
from colorsys import hsv_to_rgb
from Joystick import Joystick  # Joystick 클래스 사용
import random


class Background:
    def __init__(self, image_path="assets/background.png"):
        # Joystick 인스턴스를 통해 화면 크기 가져오기
        joystick = Joystick()
        self.__width = joystick.width
        self.__height = joystick.height

        self.__image_path = image_path  # 배경 이미지 경로
        self.__scroll_speed = 8  # 스크롤 속도
        self.__crop_point = self.__height  # 초기 스크롤 위치
        self.__fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

        # 배경 이미지 로드 및 크기 조정
        self.__image = Image.open(self.__image_path).resize((self.__width, self.__height))

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def __get_image(self):
        """
        배경 이미지를 스크롤링 방식으로 업데이트합니다.
        """
        # 스크롤 계산
        if self.__crop_point - self.__scroll_speed <= 0:
            self.__crop_point = self.__height
        else:
            self.__crop_point -= self.__scroll_speed

        # 이미지 이동
        image = Image.open(self.__image_path).resize((self.__width, self.__height))
        empty_image = Image.new("RGBA", (self.__width, self.__height))
        cropped_image1 = image.crop((0, self.__crop_point, self.__width, self.__height))
        cropped_image2 = image.crop((0, 0, self.__width, self.__crop_point))
        empty_image.paste(cropped_image1, (0, 0))
        empty_image.paste(cropped_image2, (0, self.__height - self.__crop_point))
        self.__image = empty_image
        return self.__image

    def __set_text(self, background, text):
        """
        배경에 텍스트를 추가합니다.
        """
        draw = ImageDraw.Draw(background)
        rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))  # 무작위 색상
        draw.text((38, 150), text, font=self.__fnt, fill=rcolor)

    def __call__(self):
        """
        배경 이미지 업데이트 및 오브젝트 합성.
        """
        ObjectController.renew()
        background_image = self.__get_image()

        # 플레이어 오브젝트 추가
        objects = ObjectController.getPlayerObjects()
        player, player_missiles = objects
        for info in player.items():
            player_object = info[1]
            new_image = Image.alpha_composite(background_image.crop(player_object.image_coord), player_object.image)
            background_image.paste(new_image, (player_object.image_coord[0], player_object.image_coord[1]))

        # 적 오브젝트 추가
        objects = ObjectController.getEnemyObjects()
        enemy, enemy_missiles = objects
        for info in enemy.items():
            enemy_object = info[1]
            new_image = Image.alpha_composite(background_image.crop(enemy_object.image_coord), enemy_object.image)
            background_image.paste(new_image, (enemy_object.image_coord[0], enemy_object.image_coord[1]))

        # 게임 상태 텍스트 추가
        game_text = GameSituation.getGameText()
        self.__set_text(background_image, game_text)

        return background_image
