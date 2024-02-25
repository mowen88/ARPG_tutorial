import pygame
from settings import *
from characters import NPC

class Player(NPC):
	def __init__(self, game, scene, groups, pos, z, name):
		super().__init__(game, scene, groups, pos, z, name)

		self.state = Idle(self)

	def movement(self):
		if INPUTS['left']: self.acc.x = -self.force
		elif INPUTS['right']: self.acc.x = self.force
		else: self.acc.x = 0

		if INPUTS['up']: self.acc.y = -self.force
		elif INPUTS['down']: self.acc.y = self.force
		else: self.acc.y = 0

	def vec_to_mouse(self, speed):
		direction = vec(pygame.mouse.get_pos()) - (vec(self.rect.center) - vec(self.scene.camera.offset))
		if direction.length() > 0: direction.normalize_ip()
		return direction * speed

	def exit_scene(self):
		for exit in self.scene.exit_sprites:
			if self.hitbox.colliderect(exit.rect):
				self.scene.new_scene = SCENE_DATA[int(self.scene.current_scene)][int(exit.number)]
				self.scene.entry_point = exit.number
				self.scene.transition.exiting = True

	def update(self, dt):
		self.get_direction()
		self.exit_scene()
		self.change_state()
		self.state.update(dt, self)

class Idle:
	def __init__(self, player):
		player.frame_index = 0

	def enter_state(self, player):
		if player.vel.magnitude() > 1:
			return Run(player)

		if INPUTS['right_click']:
			return Dash(player)

		if INPUTS['left_click']:
			return Attack(player)

	def update(self, dt, player):
		player.animate(f'idle_{player.get_direction()}', 15 * dt)
		player.on_floor()
		player.movement()
		player.physics(dt, player.fric)

class Run:
	def __init__(self, player):
		Idle.__init__(self, player)

	def enter_state(self, player):
		if INPUTS['right_click']:
			return Dash(player)

		if INPUTS['left_click']:
			return Attack(player)
			
		if player.vel.magnitude() < 1:
			return Idle(player)

	def update(self, dt, player):
		player.animate(f'run_{player.get_direction()}', 15 * dt)
		player.get_on_floor()
		player.movement()
		player.physics(dt, player.fric)

class Attack:
	def __init__(self, player):
		Idle.__init__(self, player)
		INPUTS['left_click'] = False
		self.timer = 0.3
		self.attack_pending = False
		self.vel = player.vec_to_mouse(80)

	def enter_state(self, player):
		if INPUTS['left_click']:
			self.attack_pending = True

		if INPUTS['right_click']:
			return Dash(player)

		if self.timer <= 0:
			if self.attack_pending:
				return Attack(player)
			else:
				return Idle(player)

	def update(self, dt, player):

		self.timer -= dt
		player.animate(f'attack_{player.get_direction()}', 15 * dt, False)
		player.physics(dt, -8)
		player.acc = vec()
		player.vel = self.vel

class Dash:
	def __init__(self, player):
		Idle.__init__(self, player)
		INPUTS['right_click'] = False
		self.timer = 0.4
		self.dash_pending = False
		self.vel = player.vec_to_mouse(200)

	def enter_state(self, player):
		if INPUTS['right_click']:
			self.dash_pending = True

		if self.timer <= 0:
			if not player.hitbox.colliderect(player.platform.rect):
				return Fall(player)
			elif self.dash_pending:
				return Dash(player)
			else:
				return Idle(player)

	def update(self, dt, player):

		self.timer -= dt
		player.animate(f'attack_{player.get_direction()}', 15 * dt, False)
		if self.timer > 0.2:
			player.physics(dt, 0)
		else:
			player.physics(dt, -30)

		player.acc = vec()
		player.vel = self.vel

class Fall:
	def __init__(self, player):
		Idle.__init__(self, player)
		self.timer = 1
		self.hitbox = player.hitbox.copy().inflate(-player.hitbox.width*0.75,-player.hitbox.height*0.75)
		self.hitbox.center = player.hitbox.center

	def enter_state(self, player):
		for platform in player.scene.platform_sprites:
			if self.hitbox.colliderect(platform.rect) or self.timer <= 0:
				return Idle(player)

		

	def update(self, dt, player):

		self.timer -= dt
		player.animate(f'fall_{player.get_direction()}', 15 * dt, False)
		player.vel = vec()
		

		