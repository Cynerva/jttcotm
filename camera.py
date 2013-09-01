from config import screen_width, screen_height

class Camera(object):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def screen_pos(self, x, y):
        x = x - self.x + screen_width / 2.0
        y = self.y - y + screen_height / 2.0
        return (x, y)
