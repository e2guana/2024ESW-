from PIL import Image

class Lifeitem:
    def __init__(self, x, y, size=30, image_path="assets/Life.png"):
        self.x = x
        self.y = y
        self.size = size
        self.image = Image.open(image_path).convert("RGBA").resize((size, size))
        self.speed = 2

    def move(self):
        self.y += self.speed

    def draw(self, base_image):
        #아이템 구현
        base_image.paste(self.image, (self.x, self.y), self.image)

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def check_collision(self, spaceship):
        item_hitbox = (self.x, self.y, self.x + self.size, self.y + self.size)
        ship_hitbox = spaceship.get_hitbox()
        return (
            item_hitbox[0] < ship_hitbox[2]
            and item_hitbox[2] > ship_hitbox[0]
            and item_hitbox[1] < ship_hitbox[3]
            and item_hitbox[3] > ship_hitbox[1]
        )