from PIL import Image
import random

class Obstacle:
    def __init__(self, width, size=30, speed=6, image_path="assets/Rock1.png"):
        self.width = width
        self.size = size
        self.speed = speed
        self.x = random.randint(0, width - size)
        self.y = -size

        # Load obstacle image
        self.image = Image.open(image_path).convert("RGBA").resize((size, size))

        # Define hitbox as 70% of the actual size
        self.hitbox_scale = 0.6
        self.hitbox_width = int(size * self.hitbox_scale)
        self.hitbox_height = int(size * self.hitbox_scale)

        # Offset for centering the hitbox
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
