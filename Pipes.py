import random
from Vector import Vector

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# handles spawning a single pipe pair
class Pipes:
    golden_counter = 0  # golden pipe tracker

    def __init__(self, width, height, pipe_width, pipe_gap, speed):
        self.width = width
        self.height = height
        self.pipe_width = pipe_width
        self.gap = pipe_gap  # gap between top and bottom
        self.speed = Vector(-speed, 0)  # movement speed of pipe

        # Randomize the gap position (where the opening is)
        self.pos = Vector(self.width + self.pipe_width / 2, 0)

        # randomize the gap position
        self.set_random_gap()

        # Pipe images
        self.pipe_bottom_img = simplegui._load_local_image('pipe.png')
        self.pipe_top_img = simplegui._load_local_image('pipe_top.png')
        self.pipe_img_width = 720
        self.pipe_img_height = 752

        # Golden pipe images
        self.gold_pipe_bottom_img = simplegui._load_local_image('gold_pipe.png')  # golden image
        self.gold_pipe_top_img = simplegui._load_local_image('gold_pipe_top.png')  # golden image

        Pipes.golden_counter += 1
        self.is_golden = Pipes.golden_counter % 20 == 0  # every 20th pipe

        # Flag to track if pipe has been passed
        self.passed = False

    def set_random_gap(self):
        # minimum distance from top and bottom of the screen
        min_distance = 80
        # calculates the center of gap
        min_val = int(min_distance + self.gap / 2)
        max_val = int(self.height - min_distance - self.gap / 2)

        # ensures min value is greater than max value
        if min_val >= max_val:
            min_val = max_val - 1

        self.gap_center = random.randint(min_val, max_val)

        # calculates top and bottom y coordinates of the gap
        self.gap_top = self.gap_center - self.gap / 2
        self.gap_bottom = self.gap_center + self.gap / 2

    def update(self):
        # moves pipe to the left
        self.pos.add(self.speed)
        # returns true if pipe is off the screen
        return self.pos.x < -self.pipe_width / 2

    def draw(self, canvas):
        pipe_draw_width = self.pipe_width * 5
        pipe_draw_height = 300

        # select correct image set
        top_img = self.gold_pipe_top_img if self.is_golden else self.pipe_top_img  # golden check
        bottom_img = self.gold_pipe_bottom_img if self.is_golden else self.pipe_bottom_img  # golden check

        # draw top pipe
        canvas.draw_image(
            top_img,
            (self.pipe_img_width / 2, self.pipe_img_height / 2),
            (self.pipe_img_width, self.pipe_img_height),
            (self.pos.x, self.gap_top - pipe_draw_height / 2),
            (pipe_draw_width, pipe_draw_height)
        )

        # draw bottom pipe
        canvas.draw_image(
            bottom_img,
            (self.pipe_img_width / 2, self.pipe_img_height / 2),
            (self.pipe_img_width, self.pipe_img_height),
            (self.pos.x, self.gap_bottom + pipe_draw_height / 2),
            (pipe_draw_width, pipe_draw_height)
        )

    def check_collision(self, bird):
        # Checks if birds is withing horizontal range of the pipe
        if (self.pos.x - self.pipe_width / 2 <= bird.pos.x + bird.radius and
                self.pos.x + self.pipe_width / 2 >= bird.pos.x - bird.radius):

            # checks if the bird is withing the gap
            if (bird.pos.y - bird.radius <= self.gap_top or
                    bird.pos.y + bird.radius >= self.gap_bottom):
                return True  # collision detected

        return False  # no collision
