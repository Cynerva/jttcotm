from Box2D import *


class World(object):
    def __init__(self):
        self.b2world = b2World(gravity=(0, -100), doSleep=True)

    def update(self, delta):
        self.b2world.Step(delta, 8, 8)
        self.b2world.ClearForces()

    def render(self, screen, camera):
        pass
