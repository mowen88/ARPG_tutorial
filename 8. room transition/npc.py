import pygame
from settings import *

class Idle:
	def enter_state(self, npc):
		if npc.vel.magnitude() > 1:
			return Run()

	def update(self, dt, npc):
		npc.animate(f'idle_{npc.get_direction()}', 15 * dt)
		npc.physics(dt)

class Run:	
	def enter_state(self, npc):
		if npc.vel.magnitude() < 1:
			return Idle()

	def update(self, dt, npc):
		npc.animate(f'run_{npc.get_direction()}', 15 * dt)
		npc.physics(dt)

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
		self.acc = pygame.math.Vector2()
		self.vel = pygame.math.Vector2()
		self.speed = 60
		self.friction = -15
		self.state = Idle()
		self.direction = self.get_direction()
		self.move = {'left':False, 'right':False, 'up':False, 'down':False}

	def get_direction(self):
		angle = self.vel.angle_to(pygame.math.Vector2(0,1))
		angle = (angle + 360) % 360
		if 45 <= angle < 135: return 'right'
		elif 135 <= angle < 225: return 'up'
		elif 225 <= angle < 315: return 'left'
		else: return 'down'

	def get_movement(self):
		if self.move['left']: self.acc.x = -2000
		elif self.move['right']: self.acc.x = 2000
		else: self.acc.x = 0

		if self.move['up']: self.acc.y = -2000
		elif self.move['down']: self.acc.y = 2000
		else: self.acc.y = 0

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
		
		self.image = self.animations[state][int(self.frame_index)]

	def get_collide_list(self, group): 
		hitlist = []
		for sprite in group:
			if sprite.hitbox.colliderect(self.hitbox): hitlist.append(sprite)
		return hitlist

	def collisions(self, direction, group):
		hitlist = self.get_collide_list(group)
		for sprite in hitlist:
			if direction == 'x':
				if self.vel.x >= 0: self.hitbox.right = sprite.hitbox.left
				if self.vel.x <= 0: self.hitbox.left = sprite.hitbox.right
				self.rect.centerx = self.hitbox.centerx
				self.pos.x = self.hitbox.centerx
			if direction == 'y':			
				if self.vel.y >= 0: self.hitbox.bottom = sprite.hitbox.top	
				if self.vel.y <= 0: self.hitbox.top = sprite.hitbox.bottom
				self.rect.centery = self.hitbox.centery
				self.pos.y = self.hitbox.centery

	def physics(self, dt):

		# x direction
		self.acc.x += self.vel.x * self.friction
		self.vel.x += self.acc.x * dt
		self.pos.x += self.vel.x * dt + (0.5 * self.vel.x) * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collisions('x', self.scene.block_sprites)

		#y direction
		self.acc.y += self.vel.y * self.friction
		self.vel.y += self.acc.y * dt
		self.pos.y += self.vel.y * dt + (0.5 * self.vel.y) * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collisions('y', self.scene.block_sprites)
		
		if self.vel.magnitude() >= self.speed: 
			self.vel = self.vel.normalize() * self.speed

	def change_state(self):
		new_state = self.state.enter_state(self)
		if new_state: self.state = new_state
		else: self.state

	def update(self, dt):
		self.get_movement()
		self.get_direction()
		self.change_state()
		self.state.update(dt, self)


