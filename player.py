import pygame
from pygame.locals import *
from Box2D import *

from debug import draw_body


class Player(object):
    def __init__(self, world, pos=(0, 0)):
        self.body = world.CreateDynamicBody(position=pos)
        self.body.CreatePolygonFixture(box=(8, 16), density=1, friction=0.0)
        self.sensor = self.body.CreatePolygonFixture(
            box=(7, 2, (0, -16), 0),
            density=1,
            friction=0.0,
            isSensor = True
        )

    @property
    def pos(self):
        return self.body.position

    def update(self, delta):
        keys = pygame.key.get_pressed()

        # Vertical logic
        if keys[K_w]:
            for ce in self.body.contacts:
                fixtureA = ce.contact.fixtureA
                fixtureB = ce.contact.fixtureB
                if self.sensor == fixtureA or self.sensor == fixtureB:
                    self.body.linearVelocity[1] = 150.0
                    break
        elif self.body.linearVelocity[1] > 0.0:
            self.body.linearVelocity[1] -= self.body.linearVelocity[1] * delta * 2.0

        # Horizontal logic
        if keys[K_a]:
            self.body.linearVelocity[0] -= 200.0 * delta
        if keys[K_d]:
            self.body.linearVelocity[0] += 200.0 * delta
        self.body.linearVelocity[0] -= self.body.linearVelocity[0] * delta * 2.0

        self.body.angle = 0.0

    def render(self, screen, camera):
        draw_body(self.body, screen, camera)
