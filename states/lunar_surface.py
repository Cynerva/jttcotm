import backgrounds
from camera import Camera


class LunarSurface(object):
    def __init__(self):
        self.background = backgrounds.LunarSurface()
        self.camera = Camera()

    def update(self, delta):
        self.background.update(delta)

    def render(self, screen):
        self.background.render(screen, self.camera)
