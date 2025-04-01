import random

from Vector import Vector
from Bird import Bird
from Background import Background
from Keyboard import Keyboard
from Powerups import Powerups
from PipeManager import PipeManager
from Button import Button
from Pipes import Pipes  # to access golden_counter

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 700
HEIGHT = 500  # Canvas Dimensions
GROUND_LEVEL = HEIGHT - 50

# Bird SpriteSheet Constants
SHEET_URL = "https://raw.githubusercontent.com/mdawood012/Flappy-Chicken/refs/heads/main/chicken.png"
SHEET_WIDTH = 800
SHEET_HEIGHT = 121
SHEET_COLUMNS = 6
SHEET_ROWS = 1

# Background constants
BACKGROUND_URL = "https://raw.githubusercontent.com/mdawood012/Flappy-Chicken/refs/heads/main/background.png"
BACKGROUND_WIDTH = 996
BACKGROUND_HEIGHT = 582
BACKGROUND_SPEED = 2

# powerups constants 
IMMUNITY_URL = "https://raw.githubusercontent.com/mdawood012/Flappy-Chicken/main/WaterBottle.png"
IMMUNITY_WIDTH = 32
IMMUNITY_HEIGHT = 32

HEART_URL = "https://github.com/clear-code-projects/ZeldaHearts/blob/master/full_heart.png?raw=true"
EMPTY_HEART_URL = "https://github.com/clear-code-projects/ZeldaHearts/blob/master/empty_heart.png?raw=true"
HEART_DIMS = (38, 32)

# Sound
GAME_OVER_S = simplegui._load_local_sound('sounds//game-over.ogg')

class Interaction:
    def __init__(self, bird, keyboard, background):
        self.bird = bird
        self.keyboard = keyboard
        self.background = background
        self.pipe_manager = PipeManager(WIDTH, HEIGHT, spawn_interval=90, speed=3)
        self.score = 0
        self.game_state = "start"
        self.counter = 0
        self.powerups_list = []
        self.check_list = []
        self.collision_processed = False
        self.high_score = 0

    def update(self):
        if self.game_state == "play":
            self.bird.update(self.keyboard)
            self.pipe_manager.update()

            if self.pipe_manager.check_collisions(self.bird) and not self.collision_processed:
                if self.bird.health > 0:
                    self.bird.get_hit()
                    self.collision_processed = True
                if self.bird.health <= 0:
                    GAME_OVER_S.play()
                    self.game_state = "over"
                    if self.score > self.high_score:
                        self.high_score = self.score
                    self.background.set_final_score(self.score)
                    self.background.set_high_score(self.high_score)
            elif not self.pipe_manager.check_collisions(self.bird):
                self.collision_processed = False

            if self.bird.pos.y >= GROUND_LEVEL:
                GAME_OVER_S.play()
                self.game_state = "over"
                if self.score > self.high_score:
                    self.high_score = self.score
                self.background.set_final_score(self.score)
                self.background.set_high_score(self.high_score)

            self.add_powerups()
            for powerup in self.powerups_list:
                powerup.update()
                powerup.collide(self.bird) 
                if powerup.collision:
                    self.bird.has_immunity = True
                    self.powerups_list.remove(powerup)
                    self.check_list.append(powerup)

            if self.bird.has_immunity and not self.pipe_manager.check_collisions(self.bird):
                self.score += self.pipe_manager.check_score(self.bird)
            elif not self.bird.has_immunity:
                self.score += self.pipe_manager.check_score(self.bird)

    def add_powerups(self):
        if (self.counter % 1000 == 0):
            powerup = Powerups(IMMUNITY_URL, IMMUNITY_WIDTH, IMMUNITY_HEIGHT, WIDTH, HEIGHT)
            self.powerups_list.append(powerup)     
        self.counter += 1

    def draw(self, canvas):
        self.update()
        if self.game_state == "play":
            self.background.update()
        self.background.draw(canvas, self.game_state)

        if self.game_state == "play":
            self.pipe_manager.draw(canvas)
            self.bird.draw(canvas)
            self.bird.hearts(canvas)
            self.bird.empty_hearts(canvas)
            for powerup in self.powerups_list:
                powerup.draw(canvas)
            canvas.draw_text(f"Score: {self.score}", (20, 40), 30, "Black")

        # ✅ removed high score drawing from here

    def restart_game(self):
        self.bird.pos = Vector(WIDTH / 3, HEIGHT / 2)
        self.bird.vel = Vector(0, 0)
        self.pipe_manager = PipeManager(WIDTH, HEIGHT, spawn_interval=90, speed=3)
        self.bird.health = 0
        self.score = 0
        self.powerups_list = []
        self.check_list = []
        self.bird.has_immunity = False
        self.collision_processed = False
        Pipes.golden_counter = 0  # reset golden pipe cycle


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
    SHEET_URL, HEART_URL, EMPTY_HEART_URL, HEART_DIMS, Vector(WIDTH / 3, HEIGHT / 2), SHEET_COLUMNS, SHEET_ROWS, SHEET_WIDTH, SHEET_HEIGHT, GROUND_LEVEL
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
