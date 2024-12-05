from PIL import Image

class Explosion:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.frames = [
            Image.open("assets/Exp2.png").convert("RGBA").resize((size, size)),
            Image.open("assets/Exp3.png").convert("RGBA").resize((size, size)),
            Image.open("assets/Exp4.png").convert("RGBA").resize((size, size)),
        ]
        self.frame_index = 0
        self.frame_delay = 2  # 프레임 유지 시간
        self.timer = 0
        self.finished = False

    def update(self):
        if not self.finished:
            self.timer += 1
            if self.timer >= self.frame_delay:
                self.timer = 0
                self.frame_index += 1
                if self.frame_index >= len(self.frames):
                    self.finished = True

    def draw(self, base_image):
        if not self.finished:
            current_frame = self.frames[self.frame_index]
            base_image.paste(current_frame, (self.x, self.y), current_frame)
