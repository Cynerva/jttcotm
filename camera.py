from config import screen_width, screen_height

class Camera(object):
    def __init__(self, pos=(0.0, 0.0), tracking=None):
        self.pos = pos
        self.vel = (0.0, 0.0)
        self.tracking = tracking

    def update(self, delta):
        if self.tracking:
            speed = delta / 8.0
            self.vel = (
                self.vel[0] + (self.tracking.pos[0] - self.pos[0]) * speed,
                self.vel[1] + (self.tracking.pos[1] - self.pos[1]) * speed
            )
        friction = delta * 8.0
        self.vel = (
            self.vel[0] * (1.0 - friction),
            self.vel[1] * (1.0 - friction)
        )
        self.pos = (
            self.pos[0] + self.vel[0],
            self.pos[1] + self.vel[1]
        )

    def screen_pos(self, pos):
        return (
            int(pos[0] - self.pos[0] + screen_width / 2),
            int(self.pos[1] - pos[1] + screen_height / 2)
        )
