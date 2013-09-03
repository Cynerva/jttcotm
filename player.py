import pygame
from pygame.locals import *
from Box2D import *

from sprite import Sprite, Animation
from debug import draw_body


class Player(object):
    def __init__(self, world, pos=(0, 0)):
        self.body = world.b2world.CreateDynamicBody(
            position=pos,
            allowSleep=False
        )
        self.body.CreatePolygonFixture(
            box=(0.8, 1.6),
            density=1,
            friction=0.0,
        )
        self.body.linearDamping = 0.0
        self.body.angularDamping = 0.0
        self.sensor = self.body.CreatePolygonFixture(
            box=(0.6, 0.2, (0, -1.6), 0),
            density=1,
            friction=0.0,
            isSensor = True
        )

        self.stand_sprite = Sprite("data/art/stand.png")
        self.jump_sprite = Sprite("data/art/jump.png")
        self.fall_sprite = Sprite("data/art/fall.png")
        walksprite0 = self.stand_sprite
        walksprite1 = Sprite("data/art/walk1.png")
        walksprite2 = Sprite("data/art/walk2.png")
        self.walk_sprite = Animation((
            walksprite0, walksprite1, walksprite1,
            walksprite0, walksprite2, walksprite2
        ))
        self.sprite = self.stand_sprite

    @property
    def pos(self):
        return tuple(self.body.position)

    def update(self, delta):
        keys = pygame.key.get_pressed()

        can_jump = False
        for ce in self.body.contacts:
            if ce.contact.touching:
                fixtureA = ce.contact.fixtureA
                fixtureB = ce.contact.fixtureB
                if self.sensor == fixtureA or self.sensor == fixtureB:
                    can_jump = True
                    break

        # Vertical logic
        if keys[K_w] and can_jump:
            self.body.linearVelocity[1] = 30.0
        elif self.body.linearVelocity[1] > 0.0:
            vel_delta = self.body.linearVelocity[1] * delta * 2.0
            self.body.linearVelocity[1] -= vel_delta

        # Horizontal logic
        if keys[K_a]:
            self.body.linearVelocity[0] -= 30.0 * delta
        if keys[K_d]:
            self.body.linearVelocity[0] += 30.0 * delta
        self.body.linearVelocity[0] -= self.body.linearVelocity[0] * delta * 2.0
            
        self.body.angle = 0.0
        self.body.angularVelocity = 0.0

        # Sprite logic
        if can_jump:
            if abs(self.body.linearVelocity[0]) > 1.0:
                self.sprite = self.walk_sprite
            else:
                self.sprite = self.stand_sprite
        elif self.body.linearVelocity[1] > 0.0:
            self.sprite = self.jump_sprite
        else:
            self.sprite = self.fall_sprite
        sprite_delta = delta * abs(self.body.linearVelocity[0]) * 2.0
        mirror = self.body.linearVelocity[0] < 0.0
        self.sprite.update(sprite_delta, mirror)

    def render(self, screen, camera):
        self.sprite.render(screen, camera, self.pos)
        #draw_body(self.body, screen, camera)
