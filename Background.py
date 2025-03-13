try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Background:
    def __init__(self, imgurl, speed, bg_width, bg_height, height):
        self.img = simplegui.load_image(imgurl)
        self.speed = speed
        self.bg_width = bg_width
        self.bg_height = bg_height
        self.height = height
        self.background_scroll = 0
    def update(self):
        self.background_scroll = (self.background_scroll + self.speed) % self.bg_width
    def draw(self, canvas):
        global background_scroll
        canvas.draw_image(self.img,
                (self.bg_width/ 2, self.bg_height / 2),
                (self.bg_width, self.bg_height),
                (self.bg_width / 2 - self.background_scroll, self.height / 2),
                (self.bg_width, self.bg_height))

        # second copy to make it continuous
        canvas.draw_image(self.img,
                        (self.bg_width / 2, self.bg_height  / 2),
                        (self.bg_width, self.bg_height ),
                        (self.bg_width * 1.5 - self.background_scroll, self.height / 2),
                        (self.bg_width, self.bg_height ))