import random

from Vector import Vector
from Bird import Bird
from Background import Background
from Keyboard import Keyboard
from PipeManager import PipeManager
from Button import Button

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
        self.pipe_manager = PipeManager(WIDTH, HEIGHT, spawn_interval=90, speed=3) # initializes pipe manager
        self.score = 0
        self.game_state = "start" # variable which tracks what mode of game were in

    def update(self):
        # if game is in "play"
        if self.game_state == "play":
            # updates bird
            self.bird.update(self.keyboard)
            # updates pipes
            self.pipe_manager.update()

            # if collision is detected then game state will change
            if self.pipe_manager.check_collisions(self.bird):
                self.game_state = "over"
                self.background.set_final_score(self.score)
                #method to allow background class to access score to display


            # if the bird hits the floor, game state will change
            if self.bird.pos.y >= GROUND_LEVEL:
                self.game_state = "over"
                self.background.set_final_score(self.score)

            # checks scoring when a bird passes a pipe. Score will increment
            self.score += self.pipe_manager.check_score(self.bird)


    def draw(self, canvas):
        # update game state
        self.update()

        # draws background
        if self.game_state == "play":
            self.background.update()

        self.background.draw(canvas,self.game_state)

        # draws pipes
        if self.game_state == "play": #pipes/bird and score only drawn when game in play
            self.pipe_manager.draw(canvas)
            self.bird.draw(canvas)
            # score counter
            canvas.draw_text(f"Score: {self.score}", (20, 40), 30, "Black")

    def restart_game(self):
        self.bird.pos = Vector(WIDTH / 2, HEIGHT / 2)
        self.bird.vel = Vector(0, 0)
        self.pipe_manager = PipeManager(WIDTH, HEIGHT, spawn_interval=90, speed=3)
        self.score = 0

#handles mouse button clicks
def mouse_handler(position):
    global inter

    if inter.background.start_button.is_clicked(position):
        inter.game_state = "play"
    if inter.background.restart_button.is_clicked(position):
        inter.game_state = "play"
        inter.restart_game()

kbd = Keyboard()
background = Background(BACKGROUND_URL, BACKGROUND_SPEED, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, HEIGHT)
bird = Bird(
    SHEET_URL, Vector(WIDTH / 2, HEIGHT / 2), SHEET_COLUMNS, SHEET_ROWS, SHEET_WIDTH, SHEET_HEIGHT, GROUND_LEVEL
)

global inter
inter = Interaction(bird, kbd, background)

frame = simplegui.create_frame("Flappy Chicken", WIDTH, HEIGHT)
frame.set_canvas_background('#88CCEE')
frame.set_draw_handler(inter.draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.set_mouseclick_handler(mouse_handler)
frame.start()
