try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

JUMP_S = simplegui._load_local_sound('sounds//jump.ogg')

class Keyboard:
    def __init__(self):
        self.jump = False
        self.just_pressed = False
    def keyDown(self, key):
        if key == simplegui.KEY_MAP['space']:
            JUMP_S.play()
            if not self.jump:
                self.just_pressed = True
            self.jump = True
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['space']:
            self.jump = False