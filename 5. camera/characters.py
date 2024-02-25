import pygame
from settings import *

class NPC(pygame.sprite.Sprite):
	def __init__(self, game, scene, groups, pos, z, name):
		super().__init__(groups)

		self.game = game
		self.scene = scene
		self.z = z
		self.name = name
		self.frame_index = 0
		self.import_images()
		self.image = self.animations['idle_down'][self.frame_index].convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5,- self.rect.height * 0.5)
		self.old_pos = self.pos.copy()
		self.old_hitbox = self.hitbox.copy()
		self.speed = 60
		self.acc = pygame.math.Vector2()
		self.vel = pygame.math.Vector2()
		self.friction = -15
		self.facing = 0
		self.alive = True
		
	def import_images(self):
		path = f'assets/characters/{self.name}/'

		self.animations = self.game.get_animation_states(path)

		for animation in self.animations.keys():
			full_path = path + animation
			self.animations[animation] = self.game.get_images(full_path)

	def animate(self, state, fps, loop=True):

		self.frame_index += fps

		if self.frame_index >= len(self.animations[state]):
			if loop: 
				self.frame_index = 0
			else:
				self.frame_index = len(self.animations[state]) -1
		
		direction = self.facing if self.facing == 1 else 0
		self.image = pygame.transform.flip(self.animations[state][int(self.frame_index)], direction-1, False)

	def physics(self, dt):

		# x direction
		self.acc.x += self.vel.x * self.friction
		self.vel.x += self.acc.x * dt
		self.pos.x += self.vel.x * dt + (0.5 * self.vel.x) * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx

		#y direction
		self.acc.y += self.vel.y * self.friction
		self.vel.y += self.acc.y * dt
		self.pos.y += self.vel.y * dt + (0.5 * self.vel.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		
		if self.vel.magnitude() >= self.speed: 
			self.vel = self.vel.normalize() * self.speed

	def update(self, dt):
		if self.vel.magnitude() < 1:
			self.animate('idle_right', 15 * dt, False)
		else:
			self.animate('run_right',15 * dt)
		self.physics(dt)

class Player(NPC):
	def __init__(self, game, scene, groups, pos, z, name):
		super().__init__(game, scene, groups, pos, z, name)

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
		if self.vel.magnitude() < 1:
			self.animate('idle_right', 15 * dt)
		else:
			self.animate('run_right',15 * dt)
		self.physics(dt)

		self.input()