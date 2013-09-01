import pygame
from pygame.locals import *
from Box2D import *

from debug import draw_body


class Player(object):
    def __init__(self, world, pos=(0, 0)):
        self.body = world.CreateDynamicBody(position=pos, allowSleep=False)
        self.body.CreatePolygonFixture(
            box=(8, 16),
            density=1,
            friction=0.0,
        )
        self.body.linearDamping = 0.0
        self.body.angularDamping = 0.0
        self.sensor = self.body.CreatePolygonFixture(
            box=(6, 2, (0, -16), 0),
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
                if ce.contact.touching:
                    fixtureA = ce.contact.fixtureA
                    fixtureB = ce.contact.fixtureB
                    if self.sensor == fixtureA or self.sensor == fixtureB:
                        self.body.linearVelocity[1] = 200.0
                        break
        elif self.body.linearVelocity[1] > 0.0:
            vel_delta = self.body.linearVelocity[1] * delta * 2.0
            self.body.linearVelocity[1] -= vel_delta

        # Horizontal logic
        if keys[K_a]:
            self.body.linearVelocity[0] -= 300.0 * delta
        if keys[K_d]:
            self.body.linearVelocity[0] += 300.0 * delta
        self.body.linearVelocity[0] -= self.body.linearVelocity[0] * delta * 2.0

        self.body.angle = 0.0
        self.body.angularVelocity = 0.0

    def render(self, screen, camera):
        draw_body(self.body, screen, camera)
