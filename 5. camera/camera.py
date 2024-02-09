import pygame
from settings import *

class Camera(pygame.sprite.Group):
    def __init__(self):

        self.offset = pygame.math.Vector2()
        self.visible_window = pygame.Rect(0,0,WIDTH*2,HEIGHT*2)

    def draw(self, screen, target, group):
        
        screen.fill(COLOURS['light green'])

        self.offset.x += target.rect.centerx - WIDTH/2 - self.offset.x
        self.offset.y += target.rect.centery - HEIGHT/2 - self.offset.y
        self.visible_window.center = target.rect.center

        for index, layer in enumerate(LAYERS):
            for sprite in group:
                if sprite.z == layer and self.visible_window.contains(sprite.rect):
                    offset = sprite.rect.topleft - self.offset
                    screen.blit(sprite.image, offset)