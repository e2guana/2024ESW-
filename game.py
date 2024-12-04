from PIL import Image, ImageDraw
from spaceship import Spaceship
from obstacle import Obstacle, Rock1, Rock2
from utils import check_collision
import random

class AstroEvasion:
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
        # Rock1 생성 확률
        if random.random() < 0.04:  # 4% 확률로 Rock1 생성
            self.obstacles.append(Rock1(self.width))

        # Rock2 생성 확률
        if random.random() < 0.02:  # 2% 확률로 Rock2 생성
            self.obstacles.append(Rock2(self.width))

    def update(self, buttons):
        self.spaceship.move(buttons)
        
        if buttons["fire"]:  # 버튼 눌리면 발사
            self.spaceship.shoot()
        
        self.spaceship.update_lasers()
        
        for obstacle in self.obstacles:
            obstacle.move()
        
        # 레이저와 장애물 충돌 처리
        lasers_to_remove = []  # 충돌한 레이저
        for laser in self.spaceship.lasers:
            for obstacle in self.obstacles:
                if check_collision(laser, obstacle):
                    obstacle.take_damage(laser.damage)
                    if obstacle.is_destroyed():
                        self.score += obstacle.get_score()  # 장애물 점수 추가
                    lasers_to_remove.append(laser)  # 충돌한 레이저 추가
                break  # 한 레이저가 한 장애물에만 영향을 줌
         # 충돌한 레이저 제거
        self.spaceship.lasers = [laser for laser in self.spaceship.lasers if laser not in lasers_to_remove]

        # 파괴된 장애물 제거
        self.obstacles = [o for o in self.obstacles if not o.is_destroyed()]
    
        # 화면 밖으로 벗어난 장애물 삭제
        self.obstacles = [o for o in self.obstacles if o.y < self.height]
        self.spaceship.lasers = [l for l in self.spaceship.lasers if not l.is_off_screen(self.height)]
        
        # 장애물과 우주선 충돌 처리
        obstacles_to_remove = []  # 충돌한 장애물
        for obstacle in self.obstacles:
            if check_collision(self.spaceship, obstacle):
                self.spaceship.take_damage()  # 우주선 체력 감소
                obstacles_to_remove.append(obstacle)  # 충돌한 장애물 추가
                if self.spaceship.is_destroyed():
                    self.game_over = True

        # 충돌한 장애물 즉시 제거
        self.obstacles = [o for o in self.obstacles if o not in obstacles_to_remove]
        
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
    
