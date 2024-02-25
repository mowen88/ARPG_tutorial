import pygame
from settings import *

class NPC(pygame.sprite.Sprite):
	def __init__(self, game, scene, groups, pos, z, name):
		super().__init__(groups)

		self.game = game
		self.scene = scene
		self.z = z
		self.name = name
		self.import_images(f'assets/characters/{self.name}/')
		self.frame_index = 0
		self.image = self.animations['idle_down'][self.frame_index].convert_alpha()
		self.rect = self.image.get_frect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(-self.rect.width/2, -self.rect.height/2)
		self.speed = 60
		self.force = 2000
		self.acc = vec()
		self.vel = vec()
		self.fric = -15
		self.move = {'left':False, 'right':False, 'up':False, 'down':False}
		self.state = Idle(self)
		self.platform = None

	def import_images(self, path):
		self.animations = self.game.get_animations(path)

		for animation in self.animations.keys():
			full_path = path + animation
			self.animations[animation] = self.game.get_images(full_path)

	def animate(self, state, fps, loop=True):
		self.frame_index += fps

		if self.frame_index >= len(self.animations[state])-1:
			if loop:
				self.frame_index = 0
			else:
				self.frame_index = len(self.animations[state])-1

		self.image = self.animations[state][int(self.frame_index)]

	def get_direction(self):
		angle = self.vel.angle_to(vec(0,1))
		angle = (angle + 360) % 360
		if 45 <= angle < 135: return 'right'
		elif 135 <= angle < 225: return 'up'
		elif 225 <= angle < 315: return 'left'
		else: return 'down'

	def on_floor(self):
		if self.platform:
			if self.hitbox.colliderect(self.platform.rect):
				return False
			else:
				return True

	def get_on_floor(self):
		for platform in self.scene.platform_sprites:
			if self.hitbox.colliderect(platform.rect):
				self.platform = platform

		if self.platform is not None:
			if self.hitbox.left < self.platform.rect.left and self.vel.x < 0:
				self.hitbox.left = self.platform.rect.left
				self.rect.centerx = self.hitbox.centerx
			elif self.hitbox.right > self.platform.rect.right and self.vel.x > 0:
				self.hitbox.right = self.platform.rect.right
				self.rect.centerx = self.hitbox.centerx
			if self.hitbox.bottom < self.platform.rect.top + 4 and self.vel.y < 0:
				self.hitbox.bottom = self.platform.rect.top + 4
				self.rect.centery = self.hitbox.centery
			elif self.hitbox.bottom > self.platform.rect.bottom - 4 and self.vel.y > 0:
				self.hitbox.bottom = self.platform.rect.bottom - 4
				self.rect.centery = self.hitbox.centery


	def movement(self):
		if self.move['left']: self.acc.x = -self.force
		elif self.move['right']: self.acc.x = self.force
		else: self.acc.x = 0

		if self.move['up']: self.acc.y = -self.force
		elif self.move['down']: self.acc.y = self.force
		else: self.acc.y = 0

	def get_collide_list(self, group):
		collidable_list = pygame.sprite.spritecollide(self, group, False)
		return collidable_list

	def collisions(self, axis, group):
		for sprite in self.get_collide_list(group):
			if self.hitbox.colliderect(sprite.hitbox):
				if axis == 'x':
					if self.vel.x >= 0: self.hitbox.right = sprite.hitbox.left
					if self.vel.x <= 0: self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
				if axis == 'y':
					if self.vel.y >= 0: self.hitbox.bottom = sprite.hitbox.top
					if self.vel.y <= 0: self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery

	def physics(self, dt, fric):
		# x direction
		self.acc.x += self.vel.x * fric
		self.vel.x += self.acc.x * dt
		self.hitbox.centerx += self.vel.x * dt + (self.vel.x/2) * dt
		self.rect.centerx = self.hitbox.centerx
		self.collisions('x', self.scene.block_sprites)

		# y direction
		self.acc.y += self.vel.y * fric
		self.vel.y += self.acc.y * dt
		self.hitbox.centery += self.vel.y * dt + (self.vel.y/2) * dt
		self.rect.centery = self.hitbox.centery
		self.collisions('y', self.scene.block_sprites)

		if self.vel.magnitude() >= self.speed:
			self.vel = self.vel.normalize() * self.speed

	def change_state(self):
		new_state = self.state.enter_state(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.get_direction()
		self.on_floor()
		self.change_state()
		self.state.update(dt, self)

class Idle:
	def __init__(self, character):
		character.frame_index = 0

	def enter_state(self, character):
		if character.vel.magnitude() > 1:
			return Run(character)

	def update(self, dt, character):
		character.animate(f'idle_{character.get_direction()}', 15 * dt)
		character.movement()
		character.physics(dt, character.fric)

class Run:
	def __init__(self, character):
		Idle.__init__(self, character)

	def enter_state(self, character):
		if character.vel.magnitude() < 1:
			return Idle(character)

	def update(self, dt, character):
		character.animate(f'run_{character.get_direction()}', 15 * dt)
		character.movement()
		character.physics(dt, character.fric)

