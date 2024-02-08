import pygame
from settings import *

class NPC(pygame.sprite.Sprite):
	def __init__(self, game, scene, groups, pos, name):
		super().__init__(groups)

		self.game = game
		self.scene = scene
		self.name = name
		self.frame_index = 0
		self.image = pygame.Surface((TILESIZE, TILESIZE*1.5))
		self.image.fill(COLOURS['white'])
		self.rect = self.image.get_rect(topleft = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 60
		self.acc = pygame.math.Vector2()
		self.vel = pygame.math.Vector2()
		self.friction = -15

	def physics(self, dt):

		# x direction
		self.acc.x += self.vel.x * self.friction
		self.vel.x += self.acc.x * dt
		self.pos.x += self.vel.x * dt + (0.5 * self.vel.x) * dt
		self.rect.centerx = round(self.pos.x)

		#y direction
		self.acc.y += self.vel.y * self.friction
		self.vel.y += self.acc.y * dt
		self.pos.y += self.vel.y * dt + (0.5 * self.vel.y) * dt
		self.rect.centery = round(self.pos.y)
		
		if self.vel.magnitude() >= self.speed: 
			self.vel = self.vel.normalize() * self.speed

	def update(self, dt):
		self.physics(dt)

class Player(NPC):
	def __init__(self, game, scene, groups, pos, name):
		super().__init__(game, scene, groups, pos, name)

	def input(self):

		if INPUTS['left']:
			self.acc.x = -2000
		elif INPUTS['right']:
			self.acc.x = 2000
		else:
			self.acc.x = 0

		if INPUTS['up']:
			self.acc.y = -2000
		elif INPUTS['down']:
			self.acc.y = 2000
		else:
			self.acc.y = 0

	def update(self, dt):
		self.physics(dt)
		self.input()