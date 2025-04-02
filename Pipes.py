

import random
from Vector import Vector


class Pipes:
    def __init__(self, width, height, pipe_width, pipe_gap, speed):
        self.width = width
        self.height = height
        self.pipe_width = pipe_width
        self.gap = pipe_gap  # gap between top and bottom
        self.speed = Vector(-speed, 0)  # movement speed of pipe
        self.vertical_speed = 3
        self.vertical_direction = 1

        # Randomize the gap position (where the opening is)
        self.pos = Vector(self.width + self.pipe_width / 2, 0)

        # randomize the gap position
        self.set_random_gap()

        self.minimum_distance = 80

        # Pipe Colors
        self.pipe_color = "Green"
        self.pipe_border = "DarkGreen"

        # Flag to track if pipe has been passed
        self.passed = False

    def set_random_gap(self):
        # minimum distance from top and bottom of the screen
        # calculates the center of gap
        minimum_distance =80
        min_val = int(minimum_distance + self.gap / 2)
        max_val = int(self.height - minimum_distance- self.gap / 2)

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

        #we got to add the speed until we are less or greater than the gap center 
        self.gap_center += self.vertical_speed * self.vertical_direction

        if self.gap_center - self.gap / 2 <= self.minimum_distance or self.gap_center + self.gap / 2 >= self.height - self.minimum_distance:
            self.vertical_direction *= -1

        #recalculate the distance. 
        self.gap_top = self.gap_center - self.gap / 2
        self.gap_bottom = self.gap_center + self.gap / 2
        # returns true if pipe is off the screen
        return self.pos.x < -self.pipe_width / 2
    

    def draw(self, canvas):
        # draw top pipe
        canvas.draw_polygon([
            (self.pos.x - self.pipe_width / 2, 0),
            (self.pos.x + self.pipe_width / 2, 0),
            (self.pos.x + self.pipe_width / 2, self.gap_top),
            (self.pos.x - self.pipe_width / 2, self.gap_top)
        ], 1, self.pipe_border, self.pipe_color)

        # draw bottom pipe
        canvas.draw_polygon([
            (self.pos.x - self.pipe_width / 2, self.gap_bottom),
            (self.pos.x + self.pipe_width / 2, self.gap_bottom),
            (self.pos.x + self.pipe_width / 2, self.height),
            (self.pos.x - self.pipe_width / 2, self.height)
        ], 1, self.pipe_border, self.pipe_color)

    def check_collision(self, bird):
        # Checks if birds is withing horizontal range of the pipe
        if (self.pos.x - self.pipe_width / 2 <= bird.pos.x + bird.radius and
                self.pos.x + self.pipe_width / 2 >= bird.pos.x - bird.radius):

            # checks if the bird is withing the gap
            if (bird.pos.y - bird.radius <= self.gap_top or
                    bird.pos.y + bird.radius >= self.gap_bottom):
                return True  # collision detected

        return False  # no collision
