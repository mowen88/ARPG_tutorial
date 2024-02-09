import pygame
from settings import *

class Object(pygame.sprite.Sprite):
	def __init__(self, groups, pos, z= 'blocks', surf=pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)

		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0,0)
		self.old_hitbox = self.hitbox.copy()
		self.z = z

class AnimatedObject(pygame.sprite.Sprite):
	def __init__(self, game, groups, pos, z, path):
		super().__init__(groups)

		self.game = game
		self.frames = self.game.get_images(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0,0)
		self.old_hitbox = self.hitbox.copy()
		self.z = z

	def animate(self, animation_speed, loop=True):
		self.frame_index += animation_speed
		self.frame_index = len(self.frames)-1 if not loop else self.frame_index % len(self.frames)
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(15 * dt)