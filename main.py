from Joystick import Joystick
from game import AstroEvasion
from PIL import Image
import time

def read_buttons(joystick):
    return {
        "up": not joystick.button_U.value,
        "down": not joystick.button_D.value,
        "left": not joystick.button_L.value,
        "right": not joystick.button_R.value,
        "fire": not joystick.button_A.value,
        "start": not joystick.button_B.value,
    }

def show_logo_screen(joystick):
    # Load and display the logo image
    logo = Image.open("assets/AstroEvasion.png")
    logo = logo.resize((joystick.width, joystick.height))
    joystick.disp.image(logo)

    print("Press A or B to start the game.")

    # Wait for A or B button press
    while True:
        buttons = read_buttons(joystick)
        if buttons["fire"] or buttons["start"]:  # A or B button pressed
            return
        time.sleep(0.1)

def main():
    joystick = Joystick()

    # Show logo screen
    show_logo_screen(joystick)

    # Start the game
    game = AstroEvasion(joystick)

    while not game.game_over:
        buttons = read_buttons(joystick)
        game.update(buttons)
        game.add_obstacle()
        game.draw()
        joystick.disp.image(game.image)
        time.sleep(0.05)

    print("Game Over! Your score:", game.score)

if __name__ == "__main__":
    main()
