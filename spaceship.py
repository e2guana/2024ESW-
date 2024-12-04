from PIL import Image, ImageDraw
from laser import Laser

class Spaceship:
    def __init__(self, width, height, size=40, image_path="assets/Me.png", life_image_path="assets/Life.png"):
        self.width = width
        self.height = height
        self.size = size
        self.x = width // 2
        self.y = height - 40
        self.speed = 6
        self.health = 3
        self.lasers = [] 
        self.laser_cooldown = 3  # 레이저 간격
        self.laser_timer = 0 

        # 우주선 이미지 로드
        self.image = Image.open(image_path).convert("RGBA").resize((size, size))
        # Life 이미지 로드 (크기 조정)
        self.life_image = Image.open(life_image_path).convert("RGBA").resize((30, 30))

    def move(self, buttons):
        if buttons["left"] and self.x > 0:
            self.x -= self.speed
        if buttons["right"] and self.x < self.width - self.size:
            self.x += self.speed
        if buttons["up"] and self.y > 0:
            self.y -= self.speed
        if buttons["down"] and self.y < self.height - self.size:
            self.y += self.speed
            
         # 레이저 발사 처리
        if buttons.get("a", False):  # Fire 버튼이 눌렸을 때
            self.shoot()

        # 레이저 쿨다운 타이머 업데이트
        if self.laser_timer > 0:
            self.laser_timer -= 1
    
    def shoot(self):
        # 레이저 발사
        if self.laser_timer == 0:
            self.lasers.append(Laser(self.x + self.size // 2, self.y))  # 레이저 중앙위치
            self.laser_timer = self.laser_cooldown

    def draw(self, base_image):
        # 우주선 구현
        base_image.paste(self.image, (self.x, self.y), self.image)

        # 레이저 구현
        for laser in self.lasers:
            laser.draw(base_image)
        
        # Life 이미지와 숫자 그리기
        x_offset = self.width - 45  # Life 이미지 X 좌표 (오른쪽 정렬)
        y_offset = self.height - 35  # Life 이미지 Y 좌표 (아래쪽 정렬)
        base_image.paste(self.life_image, (x_offset, y_offset), self.life_image)

        # 숫자 표시
        draw = ImageDraw.Draw(base_image)
        text_x = x_offset + 25  # 숫자를 이미지 바로 오른쪽에 붙여 배치
        text_y = y_offset + 10   # 숫자를 이미지와 수평으로 맞춤
        draw.text((text_x, text_y), f" {self.health}", fill=(255, 255, 255), anchor="ls")  # 큰 숫자로 표시
    
    def update_lasers(self):
        # 레이저 업데이트
        for laser in self.lasers:
            laser.move()
        self.lasers = [laser for laser in self.lasers if not laser.is_off_screen(self.height)]
    
    def take_damage(self):
        # 체력 감소
        if self.health > 0:
            self.health -= 1

    def is_destroyed(self):
        # 체력 0이면 파괴
        return self.health <= 0