import board
import digitalio
import adafruit_rgb_display.st7789 as st7789
from PIL import Image, ImageOps
from gpiozero import Button

# SPI 핀 설정
cs_pin = digitalio.DigitalInOut(board.CE0)  # Chip Select
dc_pin = digitalio.DigitalInOut(board.D25)  # Data/Command
reset_pin = digitalio.DigitalInOut(board.D24)  # Reset
spi = board.SPI()  # Hardware SPI

# 디스플레이 초기화
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    width=240,
    height=240,
    baudrate=24000000,
    x_offset=0,
    y_offset=80,
    rotation=0  # 0, 90, 180, 270 중 방향 선택
)

# 디스플레이 크기 설정
width = disp.width
height = disp.height

# 버튼 설정 (GPIO 핀 번호에 맞게 수정)
button1 = Button(5)  # Adafruit GPIO #5 → 라즈베리파이 GPIO 5
button2 = Button(6)  # Adafruit GPIO #6 → 라즈베리파이 GPIO 6

# 이미지 경로 설정
start_screen_path = "assets/AstroEvasion.png"  # 시작 화면 이미지 경로
background_path = "assets/Background.png"  # 게임 배경 화면 이미지 경로

# 이미지 로드 및 크기 조정
start_image = Image.open(start_screen_path).convert("RGB")
start_image = ImageOps.flip(start_image)  # 필요시 상하 반전
start_image = start_image.resize((width, height))

background_image = Image.open(background_path).convert("RGB")
background_image = background_image.resize((width, height))

# 디스플레이에 이미지 출력 함수
def display_image(image):
    disp.image(image)

# 시작 화면 출력
display_image(start_image)

# 버튼을 눌러 게임 화면으로 전환
try:
    while True:
        if button1.is_pressed or button2.is_pressed:
            display_image(background_image)
            break  # 화면 전환 후 루프 종료
except KeyboardInterrupt:
    pass
