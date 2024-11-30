from Joystick import Joystick

class Button:
    def __init__(self, joystick):
        self.__left = joystick.button_L
        self.__right = joystick.button_R
        self.__up = joystick.button_U
        self.__down = joystick.button_D
        self.__a = joystick.button_A
        self.__b = joystick.button_B
        self.__c = joystick.button_C

    @property
    def left(self):
        return False if self.__left.value else True

    @property
    def right(self):
        return False if self.__right.value else True

    @property
    def up(self):
        return False if self.__up.value else True

    @property
    def down(self):
        return False if self.__down.value else True

    @property
    def a(self):
        return False if self.__a.value else True

    @property
    def b(self):
        return False if self.__b.value else True

    @property
    def c(self):
        return False if self.__c.value else True
