#Maira Dawood
#Task: Create powerups 
#test here and when done add to flappy_chicken main file. 

#what i want is that when the chicken touches any of the powerups teh score doesnt go down 
from Vector import Vector

class Powerups:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector(0, 0.2)
    def update(self):
        #movement 
        pass
    def draw(self, canvas):
        #image drawn on screen
        pass
    
