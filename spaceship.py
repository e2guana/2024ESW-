from PIL import Image

class Spaceship:
    def __init__(self, width, height, size=40, image_path="assets/Me.png"):
        self.width = width
        self.height = height
        self.size = size
        self.x = width // 2
        self.y = height - 40
        self.speed = 5

        # Load spaceship image
        self.image = Image.open(image_path).convert("RGBA").resize((size, size))

    def move(self, buttons):
        if buttons["left"] and self.x > 0:
            self.x -= self.speed
        if buttons["right"] and self.x < self.width - self.size:
            self.x += self.speed
        if buttons["up"] and self.y > 0:
            self.y -= self.speed
        if buttons["down"] and self.y < self.height - self.size:
            self.y += self.speed

    def draw(self, base_image):
        # Draw the spaceship image on the base image
        base_image.paste(self.image, (self.x, self.y), self.image)
