import pygame, csv
from csv import reader
from settings import *

class Camera(pygame.sprite.Group):
    def __init__(self, scene):

        self.offset = pygame.math.Vector2()
        self.visible_window = pygame.Rect(0,0,WIDTH* 1.2,HEIGHT*1.2)
        self.scene_size = self.get_scene_size(scene)
        self.delay = 2

    def get_scene_size(self, scene):
        with open(f'scenes/0/0.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                rows = (sum (1 for row in reader) + 1)
                cols = len(row)
        return (cols * TILESIZE, rows * TILESIZE)

    def update(self, dt, target):
  
        mouse = pygame.mouse.get_pos()

        # dynamic camera movement towards mouse direction based on target sprite
        self.offset.x += (target.rect.centerx - WIDTH/2 - (WIDTH/2 - mouse[0])/2 - self.offset.x) * (self.delay * dt)
        self.offset.y += (target.rect.centery - HEIGHT/2 - (HEIGHT/2 - mouse[1])/2 - self.offset.y) * (self.delay * dt)

        # Limit offset to stop at edges
        self.offset.x = max(0, min(self.offset.x, self.scene_size[0] - WIDTH))
        self.offset.y = max(0, min(self.offset.y, self.scene_size[1] - HEIGHT))

        self.visible_window.centerx = self.offset.x + WIDTH/2
        self.visible_window.centery = self.offset.y + HEIGHT/2

    def draw(self, screen, group):

        screen.fill(COLOURS['light green'])

        for index, layer in enumerate(LAYERS):
            for sprite in group:
                if sprite.z == layer and self.visible_window.colliderect(sprite.rect):
                    offset = sprite.rect.topleft - self.offset
                    screen.blit(sprite.image, offset)