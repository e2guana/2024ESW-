from PIL import Image
import random

class Obstacle:
    def __init__(self, width, size=30, speed=5, image_path="assets/Rock1.png", health=2):
        self.width = width
        self.size = size
        self.speed = speed
        self.x = random.randint(0, width - size)
        self.y = -size
        self.health = health
         
        # 장애물 이미지 로드
        self.image = Image.open(image_path).convert("RGBA").resize((size, size))

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
        # Draw the obstacle image on the base image
        base_image.paste(self.image, (self.x, self.y), self.image)

    def get_hitbox(self):
        # Return the hitbox as a rectangle (x1, y1, x2, y2)
        return [
            self.x + self.hitbox_x_offset,
            self.y + self.hitbox_y_offset,
            self.x + self.hitbox_x_offset + self.hitbox_width,
            self.y + self.hitbox_y_offset + self.hitbox_height,
        ]
    
    def take_damage(self, damage):
        """Reduce health by damage amount."""
        self.health -= damage

    def is_destroyed(self):
        """Check if the obstacle is destroyed."""
        return self.health <= 0


class Rock1(Obstacle):
    def __init__(self, width):
        super().__init__(width, size=30, speed=5, image_path="assets/Rock1.png",  health=2)


class Rock2(Obstacle):
    def __init__(self, width):
        super().__init__(width, size=35, speed=3, image_path="assets/Rock2.png", health=4)
