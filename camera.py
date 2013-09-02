from config import screen_width, screen_height

class Camera(object):
    def __init__(self, pos=(0.0, 0.0)):
        self.pos = pos

    def screen_pos(self, pos):
        return (
            int(pos[0] - self.pos[0] + screen_width / 2),
            int(self.pos[1] - pos[1] + screen_height / 2)
        )
