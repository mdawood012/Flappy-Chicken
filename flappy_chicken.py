import random

from Vector import Vector
from Bird import Bird
from Background import Background
from Keyboard import Keyboard
from PipeManager import PipeManager

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
        self.game_active = True # flag which keep track of game active state

    def update(self):
        if self.game_active:
            # updates bird if game is active
            self.bird.update(self.keyboard)
            # updates pipes
            self.pipe_manager.update()

            # if collision is detected then game state will change
            if self.pipe_manager.check_collisions(self.bird):
                self.game_active = False

            # if the bird hits the floor, game state will change
            if self.bird.pos.y >= GROUND_LEVEL:
                self.game_active = False

            # checks scoring when a bird passes a pipe. Score will increment
            self.score += self.pipe_manager.check_score(self.bird)

    def draw(self, canvas):
        # update game state
        self.update()

        # draws background
        self.background.update()
        self.background.draw(canvas)

        # draws pipes
        self.pipe_manager.draw(canvas)

        self.bird.draw(canvas)

        # floor line
        canvas.draw_line((0, GROUND_LEVEL), (WIDTH, GROUND_LEVEL), 2, "Brown")
        # score counter
        canvas.draw_text(f"Score: {self.score}", (20, 40), 30, "White")

        # death message when game state is flipped
        if not self.game_active:
            canvas.draw_text("Game Over", (WIDTH / 2 - 100, HEIGHT / 2), 50, "Red")
            canvas.draw_text("Press space to restart", (WIDTH / 2 - 120, HEIGHT / 2 + 50), 30, "White")

            # if keyboard is pressed the game will restart
            if self.keyboard.just_pressed:
                self.restart_game()

    def restart_game(self):
        self.bird.pos = Vector(WIDTH / 2, HEIGHT / 2)
        self.bird.vel = Vector(0, 0)
        self.pipe_manager = PipeManager(WIDTH, HEIGHT, spawn_interval=90, speed=3)
        self.score = 0
        self.game_active = True
        self.keyboard.just_pressed = False


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
