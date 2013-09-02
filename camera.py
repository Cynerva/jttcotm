from config import screen_width, screen_height

class Camera(object):
    def __init__(self):
        self.pos = (0.0, 0.0)

    def screen_pos(self, x, y):
        x = x - self.pos[0] + screen_width / 2.0
        y = self.pos[1] - y + screen_height / 2.0
        return (x, y)
