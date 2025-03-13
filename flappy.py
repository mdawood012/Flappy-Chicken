import random

from Vector import Vector
from Bird import Bird
from Background import Background
from Keyboard import Keyboard

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 700
HEIGHT = 500  # Canvas Dimensions
GROUND_LEVEL = HEIGHT - 50

# Bird SpriteSheet Constants
SHEET_URL = "https://media-hosting.imagekit.io//d248eb0cc6e34f7c/chicken.png?Expires=1836389273&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=yl~aFjJCwcsBNSUaNosFZOYKFVJR9kV4DW1xW5T15VYfGYWh6wrlxM39c0E~lpLF8srGIYEuxy0rkXnPnV-R-K13c2VHnjl2G4c6SpnhKUMuzihhfKy~~EZHBLBtW1ve1px2xmjGDynhWELRutPFeG3CSRKmuX2mvOdEZj59eIFAZpMH0dveBmqc9nrn-PSKtT4BEGHcqGLYHX6-2gXIrB2hKYD5VQm2hnmr56zM7mJqSFqRttPWMczU0mz~HZ-5ROJ5qm6673XqSMQijrSg90m106rBQ4GlxAV0UB0Fgomx841HcKKC31FdcYEKA1eYsVcUxhXss1~7ORplry1W8g__"
SHEET_WIDTH = 800
SHEET_HEIGHT = 121
SHEET_COLUMNS = 6
SHEET_ROWS = 1

# Background constants
BACKGROUND_URL = "https://raw.githubusercontent.com/mdawood012/Flappy-Chicken/refs/heads/main/background.png"
BACKGROUND_WIDTH = 996
BACKGROUND_HEIGHT = 582
BACKGROUND_SPEED = 2

class Interaction:
    def __init__(self, bird, keyboard, background):
        self.bird = bird
        self.keyboard = keyboard
        self.background = background

    def update(self):
        self.bird.update(self.keyboard)

    def draw(self, canvas):
        self.update()
        self.background.update()
        self.background.draw(canvas)
        self.bird.draw(canvas)



kbd = Keyboard()
background = Background(BACKGROUND_URL, BACKGROUND_SPEED, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, HEIGHT)
bird = Bird(
    SHEET_URL, Vector(WIDTH / 2, HEIGHT / 2), SHEET_COLUMNS, SHEET_ROWS, SHEET_WIDTH, SHEET_HEIGHT, GROUND_LEVEL
)

inter = Interaction(bird, kbd, background)

frame = simplegui.create_frame("Flappy Chicken", WIDTH, HEIGHT)
frame.set_canvas_background('#88CCEE')
frame.set_draw_handler(inter.draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
