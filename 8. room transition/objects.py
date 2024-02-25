import pygame
from settings import *

class Collider(pygame.sprite.Sprite):
	def __init__(self, groups, pos, size, name):
		super().__init__(groups)

		self.image = pygame.Surface((size))
		self.rect = self.image.get_frect(topleft = pos)
		self.name = name

class Object(pygame.sprite.Sprite):
	def __init__(self, groups, pos, z= 'blocks', surf=pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)

		self.z = z
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0,0)
		self.old_hitbox = self.hitbox.copy()
		
class Wall(Object):
	def __init__(self, groups, pos, z, surf):
		super().__init__(groups, pos, z, surf)
		self.hitbox = self.rect.copy().inflate(0, -self.rect.height * 0.5)

class AnimatedObject(pygame.sprite.Sprite):
	def __init__(self, game, groups, pos, z, path):
		super().__init__(groups)

		self.game = game
		self.z = z
		self.frames = self.game.get_images(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0,0)
		self.old_hitbox = self.hitbox.copy()

	def animate(self, animation_speed, loop=True):
		self.frame_index += animation_speed
		self.frame_index = len(self.frames)-1 if not loop else self.frame_index % len(self.frames)
		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(15 * dt)