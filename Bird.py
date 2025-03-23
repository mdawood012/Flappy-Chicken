import math

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from Vector import Vector


class Bird:
    def __init__(self, imgurl, heart_url, empty_url, heart_dims, pos, columns, rows, obj_width, obj_height, ground_level):
        self.pos = pos
        self.img = simplegui.load_image(imgurl)
        self.vel = Vector(0, 0)
        self.gravity = Vector(0, 0.6)
        self.jump_strength = Vector(0, -10)
        self.radius = 40

        self.columns = columns
        self.rows = rows
        self.obj_width = obj_width
        self.obj_height = obj_height
        self.ground_level = ground_level
        self.frame_width = self.obj_width / self.columns
        self.frame_height = self.obj_height / self.rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

        self.frame_index = [0, 0]
        self.frame_delay = 5
        self.frame_counter = 0

        # for the lives in immunity powerup
        self.heart_image = simplegui.load_image(heart_url)
        self.empty_heart_image = simplegui.load_image(empty_url)
        self.heart_dims = heart_dims
        self.has_immunity = False
        self.health = 0
        self.max_health = 3
    def draw(self, canvas):
        # animation frame update
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.next_frame()

        # calculates source center
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x + 1,
            self.frame_height * self.frame_index[1] + self.frame_centre_y + 1
        )
        source_size = (self.frame_width, self.frame_height)
        dest_centre = self.pos.get_p()
        dest_size = (100, 100)

        # Draws sprite frame
        canvas.draw_image(
            self.img,
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

        if self.pos.y > self.ground_level:
            self.pos.y = self.ground_level
            self.vel.y = 0
        if self.pos.y < self.radius:
            self.pos.y = self.radius
            self.vel.y = 0
    def get_hit(self):
        if self.health > 0:
            self.health -= 1
    def hearts(self, canvas):
        self.heart_dims = (38, 32)  # Set size of heart
        for heart in range(self.health):  # Assuming self.health is the number of hearts
            x = 580 + (heart * 40)  
            y = 20
            canvas.draw_image(self.heart_image, (self.heart_dims[0] / 2, self.heart_dims[1] / 2), self.heart_dims, (x, y), self.heart_dims)
    def empty_hearts(self, canvas):
        self.heart_dims = (38, 32)  # Set size of heart
        if self.health < self.max_health:
            for heart in range(self.max_health - self.health):
                x = 580 + ((self.max_health - heart - 1) * 40)
                y = 20
                canvas.draw_image(self.empty_heart_image, (self.heart_dims[0] / 2, self.heart_dims[1] / 2), self.heart_dims, (x, y), self.heart_dims)
