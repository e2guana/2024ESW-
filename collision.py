from PIL import Image
import time

class Collision:
    def __init__(self, x, y, duration=0.5, image_path="assets/Collision.png"):
        self.x = x
        self.y = y
        self.image = Image.open(image_path).convert("RGBA").resize((20, 20))
        self.start_time = time.time()
        self.duration = duration #충돌 표시 지속시간

    def is_active(self):
        # 충돌 상태 체크
        return time.time() - self.start_time < self.duration

    def draw(self, base_image):
        #충돌 표시 생성
        base_image.paste(self.image, (self.x, self.y), self.image)

