import random

from config import screen_width, screen_height


class Starfield(object):
    class Star(object):
        def __init__(self):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            self.pos = (x, y)
            self.r = random.randint(192, 255)
            self.g = random.randint(192, 255)
            self.b = random.randint(192, 255)
            self.brightness = random.uniform(0.5, 1.0)
            self.flicker = random.uniform(0.5, 1.0)

        def update(self, delta):
            self.flicker += random.uniform(-10.0, 10.0) * delta
            self.flicker = max(0.5, min(1.0, self.flicker))

        def render(self, screen):
            m = self.brightness * self.flicker
            color = (self.r * m, self.g * m, self.b * m)
            screen.set_at(self.pos, color)

    def __init__(self):
        self.stars = [Starfield.Star() for _ in range(256)]

    def update(self, delta):
        for star in self.stars:
            star.update(delta)

    def render(self, screen, camera):
        for star in self.stars:
            star.render(screen)
