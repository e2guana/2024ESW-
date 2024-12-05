from PIL import Image
from collision import Collision
import random

class Obstacle:
    def __init__(self, width, size=30, speed=5, image_path="assets/Rock1.png", health=2, score=10):
        self.width = width
        self.size = size
        self.speed = speed
        self.x = random.randint(0, width - size)
        self.y = -size
        self.health = health
        self.score = score    # 장애물 파괴 시 점수
        self.image = Image.open(image_path).convert("RGBA").resize((size, size))  # 장애물 이미지 로드
        self.is_destroyed = False
        
        # self.collision = None  # 충돌 표시 객체
        
        # 히트박스 구현
        self.hitbox_scale = 0.7
        self.hitbox_width = int(size * self.hitbox_scale)
        self.hitbox_height = int(size * self.hitbox_scale)

        # 히트박스가 물체 중앙에 오도록 함
        self.hitbox_x_offset = (size - self.hitbox_width) // 2
        self.hitbox_y_offset = (size - self.hitbox_height) // 2

    def move(self):
        self.y += self.speed

    def draw(self, base_image):
        base_image.paste(self.image, (self.x, self.y), self.image)
        

    def get_hitbox(self):
        # 히트박스 반환
        return [
            self.x + self.hitbox_x_offset,
            self.y + self.hitbox_y_offset,
            self.x + self.hitbox_x_offset + self.hitbox_width,
            self.y + self.hitbox_y_offset + self.hitbox_height,
        ]
    
    def handle_collision(self, spaceship, collisions):
        # 방어막이 없을 때만 충돌 처리
        if not self.collision and not spaceship.barrier.is_active:
            collision_x = self.x + self.size // 2 - 20
            collision_y = self.y + self.size // 2 - 20
            self.collision = Collision(collision_x, collision_y)
            collisions.append(self.collision)  # 충돌 표시 리스트에 추가
    
    def take_damage(self, damage):
        # 데미지 받으면 체력 감소
        self.health -= damage
        if self.health <= 0:
                self.is_destroyed = True

    def is_destroyed(self):
        #장애물 파괴 감지
        return self.health <= 0
    
    def get_score(self):
        # 장애물 파괴시 점수 반환
        return self.score


class Rock1(Obstacle):
    def __init__(self, width):
        super().__init__(width, size=30, speed=5, image_path="assets/Rock1.png",  health=2, score=40)

class Rock2(Obstacle):
    def __init__(self, width):
        super().__init__(width, size=35, speed=3, image_path="assets/Rock2.png", health=4, score=70)