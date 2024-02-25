import pygame
from settings import *
from characters import NPC

class Player(NPC):
	def __init__(self, game, scene, groups, pos, z, name):
		super().__init__(game, scene, groups, pos, z, name)

		self.get_start_direction()
		self.state = Idle(self)

	def get_start_direction(self):
		if self.rect.centerx < TILESIZE * 3: self.vel.x = 1
		elif self.rect.centerx > TILESIZE * 3: self.vel.x = -1
		elif self.rect.centery < HEIGHT: self.vel.y = 1
		else: self.vel.y = -1

	def movement(self):
		if INPUTS['left']: self.acc.x = -self.force
		elif INPUTS['right']: self.acc.x = self.force
		else: self.acc.x = 0

		if INPUTS['up']: self.acc.y = -self.force
		elif INPUTS['down']: self.acc.y = self.force
		else: self.acc.y = 0

	def exit_scene(self):
		for exit in self.scene.exit_sprites:
			if self.hitbox.colliderect(exit.rect):
				self.scene.new_scene = SCENE_DATA[int(self.scene.current_scene)][int(exit.name)]
				self.scene.entry_point = exit.name
				self.scene.transition.exiting = True

	def vec_to_mouse(self, speed):
	    # Calculate direction vector towards mouse
	    direction = vec(pygame.mouse.get_pos()) - (vec(self.rect.center) - vec(self.scene.camera.offset))
	    if direction.length() > 0: direction.normalize_ip()
	    return direction * speed

	def update(self, dt):
		self.get_direction()
		self.exit_scene()
		self.change_state()
		self.state.update(dt, self)
		

class Idle:
	def __init__(self, player):
		player.frame_index = 0

	def enter_state(self, player):
		
		if INPUTS['right_click']:
			return Dash(player)

		if player.vel.magnitude() > 1:
			return Run(player)

	def update(self, dt, player):
		player.animate(f'idle_{player.get_direction()}', 15 * dt)
		player.movement()
		player.physics(dt, player.friction)

class Run:
	def __init__(self, player):
		Idle.__init__(self, player)

	def enter_state(self, player):

		if INPUTS['right_click']:
			return Dash(player)

		if player.vel.magnitude() < 1:
			return Idle(player)

	def update(self, dt, player):
		player.animate(f'run_{player.get_direction()}', 15 * dt)
		player.movement()
		player.physics(dt, player.friction)

class Dash:
	def __init__(self, player):
		Idle.__init__(self, player)
		INPUTS['right_click'] = False
		self.timer = 0.5
		self.dash_pending = False
		#self.vel = vec(self.mouse, player.hitbox.center - player.scene.camera.offset).normalize() * self.speed
		self.vel = player.vec_to_mouse(200)

	def enter_state(self, player):
		if INPUTS['right_click']:
			self.dash_pending = True
			
		if self.timer < 0:
			if self.dash_pending:
				return Dash(player)
			else:
				return Idle(player)

	def update(self, dt, player):

		self.timer -= dt
		player.animate(f'attack_{player.get_direction()}', 15 * dt, False)

		player.physics(dt, -5)
		player.acc = vec()
		player.vel = self.vel