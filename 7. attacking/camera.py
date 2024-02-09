import pygame, csv
from csv import reader
from settings import *

class Camera(pygame.sprite.Group):
    def __init__(self, scene):

        self.offset = pygame.math.Vector2()
        self.visible_window = pygame.Rect(0,0,WIDTH*2,HEIGHT*2)
        self.scene_size = self.get_scene_size(scene)

    def get_scene_size(self, scene):
        with open(f'scenes/0/0.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                rows = (sum (1 for row in reader) + 1)
                cols = len(row)
        return (cols * TILESIZE, rows * TILESIZE)

    def draw(self, screen, target, group):

        screen.fill(COLOURS['light green'])

        self.offset.x += target.rect.centerx - WIDTH/2 - self.offset.x
        self.offset.y += target.rect.centery - HEIGHT/2 - self.offset.y
        self.visible_window.center = target.rect.center

        #limit offset to stop at edges
        if self.offset[0] < 0: self.offset[0] = 0
        elif self.offset[0] > self.scene_size[0] - WIDTH: self.offset[0] = self.scene_size[0] - WIDTH
        if self.offset[1] < 0: self.offset[1] = 0
        elif self.offset[1] > self.scene_size[1] - HEIGHT: self.offset[1] = self.scene_size[1] - HEIGHT

        for index, layer in enumerate(LAYERS):
            for sprite in sorted(group, key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer and self.visible_window.contains(sprite.rect):
                    offset = sprite.rect.topleft - self.offset
                    screen.blit(sprite.image, offset)