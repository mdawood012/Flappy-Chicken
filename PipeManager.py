from Pipes import Pipes
import random

# handles spawning multiple pipes
class PipeManager:
    def __init__(self, width, height, spawn_interval=90, speed=3):
        self.width = width
        self.height = height
        self.pipes = []
        self.spawn_interval = spawn_interval  # Frames between pipe spawns
        self.frame_counter = 0
        self.pipe_speed = speed

        # Pipe specifications
        self.pipe_width = 80
        self.min_gap = 220  # Minimum gap between pipes
        self.max_gap = 240  # Maximum gap between pipes

    def update(self):
        # Spawn new pipes at intervals
        self.frame_counter += 1
        if self.frame_counter >= self.spawn_interval:
            self.frame_counter = 0
            gap_size = random.randint(self.min_gap, self.max_gap)
            self.pipes.append(Pipes(self.width, self.height, self.pipe_width, gap_size, self.pipe_speed))

        # Update pipes and remove off-screen ones
        pipes_to_remove = []
        for pipe in self.pipes:
            if pipe.update():  # Returns True if pipe is off-screen
                pipes_to_remove.append(pipe)

        # Remove pipes that are off the screen
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)

    def draw(self, canvas):
        for pipe in self.pipes:
            pipe.draw(canvas)

    def check_collisions(self, bird):
        for pipe in self.pipes:  # loop through pipes and if a collision is detected returns state
            if pipe.check_collision(bird):
                return True  # Collision detected
        return False  # No collision

    def check_score(self, bird):
        score_update = 0
        for pipe in self.pipes:  # loops through pipes and if the bird passed the pipe it will be counted
            if bird.pos.x > pipe.pos.x and not pipe.passed:
                pipe.passed = True
                score_update += 5 if pipe.is_golden else 1  # golden pipe bonus
        return score_update
