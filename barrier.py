import time
from PIL import Image, ImageDraw

class Barrier:
    def __init__(self, uses=5, duration=4, effect_image_path="assets/barrier2.png", icon_image_path="assets/barrier.png"):
        self.uses = uses  # 방어막 사용 가능 횟수
        self.duration = duration  # 방어막 지속 시간
        self.is_active = False  # 방어막 활성화 상태
        self.start_time = 0  # 방어막 시작 시간

        # 이미지 로드
        self.effect_image = Image.open(effect_image_path).convert("RGBA"). resize((41,41))
        self.icon_image = Image.open(icon_image_path).convert("RGBA").resize((16, 16))

    def activate(self):
        # 방어막 활성화
        if self.uses > 0 and not self.is_active:
            self.is_active = True  # 방어막 활성화
            self.start_time = time.time()  # 방어막 시작 시간 기록
            self.uses -= 1  # 사용 가능 횟수 감소

    def deactivate(self):
        # 지속시간 경과 후 비활성화
        if self.is_active and time.time() - self.start_time >= self.duration:
            self.is_active = False  # 방어막 비활성화

    def draw_effect(self, base_image, x, y):
        #방어막 이펙트
        if self.is_active:  # 방어막이 활성화된 경우에만 그리기
            # 방어막 이미지의 중심을 우주선 중심에 맞춤
            effect_x = x + (self.effect_image.width // 2) - (self.effect_image.width // 2)
            effect_y = y + (self.effect_image.height // 2) - (self.effect_image.height // 2)
            base_image.paste(self.effect_image, (effect_x, effect_y), self.effect_image)

    def draw_icon(self, base_image, x, y):
        # 아이콘 표시
        base_image.paste(self.icon_image, (x, y), self.icon_image)
        # 남은 횟수 텍스트 표시
        draw = ImageDraw.Draw(base_image)
        draw.text((x + 24, y + 2), f"{self.uses}", fill=(255, 255, 255), align="center")
