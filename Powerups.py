from Vector import Vector
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    

class Powerups:
    def __init__(self, imgurl, obj_width, obj_height, width, height):
        self.img = simplegui.load_image(imgurl)
        self.obj_width = obj_width
        self.obj_height = obj_height
        self.width = width
        self.height = height
        self.pos = Vector(random.randint(200, 600), 10)
        self.vel = Vector(0.40, 1)
        self.collision = False
        self.checker = self.pos.x < self.width//2
    def update(self):
        if self.checker:
            self.pos.add(self.vel)
        else:
            self.pos.add(Vector(-2, 1))
    def collide(self, bird):
        if not self.collision:
            distance = self.pos.copy().subtract(bird.pos).length()
            if distance < (self.height/8):
                self.collision = True
                bird.health = 3
    def draw(self, canvas):
        if not self.collision:
            center_source = (self.obj_width // 2, self.obj_height // 2)
            center_dest = self.pos.get_p()
            size_source = (self.obj_width, self.obj_height)
            size_dest = (self.width/20, self.height/20)
            canvas.draw_image(self.img, center_source, size_source, center_dest, size_dest)


