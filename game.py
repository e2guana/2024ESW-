from PIL import Image, ImageDraw
from spaceship import Spaceship
from obstacle import Obstacle
from utils import check_collision
import random

class SpaceshipGame:
    def __init__(self, joystick):
        self.joystick = joystick
        self.width = joystick.width
        self.height = joystick.height
        self.image = Image.new("RGB", (self.width, self.height))
        self.spaceship = Spaceship(self.width, self.height)
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.background = Image.open("assets/Background.png").resize((self.width, self.height))

    def add_obstacle(self):
        if random.random() < 0.02:  # 장애물 생성 확률
            self.obstacles.append(Obstacle(self.width))

    def update(self, buttons):
        self.spaceship.move(buttons)
        for obstacle in self.obstacles:
            obstacle.move()
        # 화면 밖으로 벗어난 장애물 삭제
        self.obstacles = [o for o in self.obstacles if o.y < self.height]
        # 충돌 검사
        for obstacle in self.obstacles:
            if check_collision(self.spaceship, obstacle):
                self.game_over = True
        # 점수 업데이트
        self.score += 1

    def draw(self):
        # 새 이미지로 그리기 초기화
        self.image.paste(self.background, (0, 0))  # 배경 이미지 설정
        draw = ImageDraw.Draw(self.image)  # 이미지에 그리기 객체 생성

        # 우주선 그리기
        self.spaceship.draw(self.image)
        # 장애물 그리기
        for obstacle in self.obstacles:
            obstacle.draw(self.image)
        # 점수 표시
        draw.text((10, 10), f"Score: {self.score}", fill=(255, 255, 255))  # 흰색 텍스트
