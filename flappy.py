import random
try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

class Spritesheet:
    def __init__(self, imgurl, width, height, columns, rows):
        self.img = simplegui.load_image(imgurl)
        self.rows = rows
        self.columns = columns
        
        self.frame_width = width / columns
        self.frame_height = height / rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        
        self.frame_index = [0,0]
        
    def draw(self, canvas):
        #self.next_frame()
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )
        source_size = (self.frame_width, self.frame_height)
        dest_centre = (300, 150)
        dest_size = (100, 100)
        canvas.draw_image(
            self.img, source_centre, source_size,
            dest_centre, dest_size
        )
    def next_frame(self):
        self.frame_index[0] += 1
        if (self.frame_index[0]+1) % self.columns == 0:
            self.frame_index[0] = 0
            self.frame_index[1] += 1
            if (self.frame_index[1]) % self.rows == 0:
                self.frame_index[1] = 0

class Clock:
    def __init__(self):
        self.time = 0
    def tick(self):
        self.time += 1
    def transition(self, frame_duration):
        if frame_duration == self.time:
            self.time = 0
            return True
def draw(canvas):
    clock.tick()
    sheet.draw(canvas)
    if clock.transition(2):
        sheet.next_frame()

SHEET_URL = "http://www.cs.rhul.ac.uk/courses/CS1830/sprites/runnerSheet.png"
SHEET_WIDTH = 1440
SHEET_HEIGHT = 1480
SHEET_COLUMNS = 6
SHEET_ROWS = 5  

frame = simplegui.create_frame("Sprite", 600, 300)  
sheet = Spritesheet(
    SHEET_URL, SHEET_WIDTH, SHEET_HEIGHT,
    SHEET_COLUMNS, SHEET_ROWS
)
clock = Clock()
frame.set_draw_handler(draw)
frame.start()

