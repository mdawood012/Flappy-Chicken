import random

from Vector import Vector

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 800
HEIGHT = 700  # Canvas Dimensions
GROUND_LEVEL = HEIGHT - 50

# Bird SpriteSheet Constants
SHEET_URL = "https://images.freeimages.com/vhq/images/previews/5c5/flapping-chicken-sprite-sheet-102255.png?fmt=webp&h=350"
SHEET_WIDTH = 800
SHEET_HEIGHT = 121
SHEET_COLUMNS = 6
SHEET_ROWS = 1

# Background constants
BACKGROUND_URL = "https://img.freepik.com/free-vector/cartoon-fantastic-forest-landscape-nature-panorama-game-liana-covering-grass-landscape-game-vector-illustration_1284-47784.jpg?t=st=1741631334~exp=1741634934~hmac=f70b149e274e7bcf0204eaae274350caf8631f7d01a54618cb678cd0b96b8751&w=1060"
background = simplegui.load_image(BACKGROUND_URL)
background_scroll = 0
BACKGROUND_SPEED = 2


class Bird:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector(0, 0)
        self.gravity = Vector(0, 0.6)
        self.jump_strength = Vector(0, -15)
        self.radius = 40

        self.sheet = simplegui.load_image(SHEET_URL)
        self.columns = SHEET_COLUMNS
        self.rows = SHEET_ROWS

        self.frame_width = SHEET_WIDTH / self.columns
        self.frame_height = SHEET_HEIGHT / self.rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

        self.frame_index = [0, 0]
        self.frame_delay = 5
        self.frame_counter = 0

    def draw(self, canvas):
        # animation frame update
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.next_frame()

        # calculates source center
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )
        source_size = (self.frame_width, self.frame_height)
        dest_centre = self.pos.get_p()
        dest_size = (100, 100)

        # Draws sprite frame
        canvas.draw_image(
            self.sheet,
            source_centre, source_size,
            dest_centre, dest_size
        )

    def next_frame(self):
        # Move to next frame in spritesheet
        self.frame_index[0] = (self.frame_index[0] + 1) % self.columns

    def update(self, keyboard):
        if keyboard.just_pressed:
            self.vel = self.jump_strength.copy()
            keyboard.just_pressed = False

        self.vel.add(self.gravity)
        self.pos.add(self.vel)

        if self.pos.y > GROUND_LEVEL:
            self.pos.y = GROUND_LEVEL
            self.vel.y = 0
        if self.pos.y < self.radius:
            self.pos.y = self.radius
            self.vel.y = 0


class Keyboard:
    def __init__(self):
        self.jump = False
        self.just_pressed = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['space']:
            if not self.jump:
                self.just_pressed = True
            self.jump = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['space']:
            self.jump = False


class Interaction:
    def __init__(self, bird, keyboard):
        self.bird = bird
        self.keyboard = keyboard

    def update(self):
        self.bird.update(self.keyboard)


kbd = Keyboard()
bird = Bird(Vector(WIDTH / 2, HEIGHT / 2))
inter = Interaction(bird, kbd)


def draw(canvas):
    global background_scroll

    # Scroll background
    background_scroll = (background_scroll + BACKGROUND_SPEED) % background.get_width()

    # first copy of background
    canvas.draw_image(background,
                      (background.get_width() / 2, background.get_height() / 2),
                      (background.get_width(), background.get_height()),
                      (background.get_width() / 2 - background_scroll, HEIGHT / 2),
                      (background.get_width(), background.get_height()))

    # second copy to make it continuous
    canvas.draw_image(background,
                      (background.get_width() / 2, background.get_height() / 2),
                      (background.get_width(), background.get_height()),
                      (background.get_width() * 1.5 - background_scroll, HEIGHT / 2),
                      (background.get_width(), background.get_height()))

    inter.update()
    bird.draw(canvas)


frame = simplegui.create_frame("Flappy Chicken", WIDTH, HEIGHT)
frame.set_canvas_background('#88CCEE')
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
