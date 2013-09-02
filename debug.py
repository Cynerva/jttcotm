import pygame

def draw_body(body, screen, camera):
    touching = set()
    for contact_edge in body.contacts:
        contact = contact_edge.contact
        if contact.touching:
            touching.add(contact.fixtureA)
            touching.add(contact.fixtureB)
    for fixture in body.fixtures:
        shape = fixture.shape
        vertices = [
            camera.screen_pos(body.transform * x)
            for x in shape.vertices
        ]
        color = (255, 255, 255)
        if fixture.sensor:
            if fixture in touching:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
        pygame.draw.polygon(screen, color, vertices, 1)
