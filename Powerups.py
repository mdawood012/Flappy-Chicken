#Maira Dawood
#Task: Create powerups 
#test here and when done add to flappy_chicken main file. 

#what i want is that when the chicken touches any of the powerups teh score doesnt go down 
from Vector import Vector

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    

class Powerups:
    def __init__(self, imgurl, pos, obj_width, obj_height, width, height):
        self.img = simplegui.load_image(imgurl)
        self.pos = pos
        self.obj_width = obj_width
        self.obj_height = obj_height
        self.width = width
        self.height = height
        self.vel = Vector(0, 0.2)
    def update(self):
        self.pos.add(self.vel)
    def collide(self, chicken):
        distance = self.pos.copy().subtract(chicken.pos).length()
        return distance < self.obj_width/2 + chicken.obj_width/2     
    def draw(self, canvas):
        center_source = (self.obj_width // 2, self.obj_height // 2)
        center_dest = self.pos.get_p()
        size_source = (self.obj_width, self.obj_height)
        size_dest = (self.width/20, self.height/20)
        canvas.draw_image(self.img, center_source, size_source, center_dest, size_dest)
    
