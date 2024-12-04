from PIL import Image, ImageDraw

class Laser:
    def __init__(self, x, y, speed=15, damage=1, image_path="assets/Laser_me.png"):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        
         # Load laser image
        self.image = Image.open(image_path).convert("RGBA").resize((10, 20))
        self.width, self.height = self.image.size  # 이미지 크기를 속성으로 저장
         
    def move(self):
        """Move the laser upward."""
        self.y -= self.speed

    def draw(self, base_image):
        """Draw the laser image on the base image."""
        base_image.paste(self.image, (self.x - self.width // 2, self.y), self.image)

    def is_off_screen(self, screen_height):
        """Check if the laser is off the screen."""
        return self.y + self.height < 0
