import pygame
from settings import *
from npc import NPC

class Idle:
	def enter_state(self, player):
		if player.vel.magnitude() > 1:
			return Run()

	def update(self, dt, player):
		player.animate(f'idle_{player.get_direction()}', 15 * dt)
		player.input()
		player.physics(dt)

class Run:	
	def enter_state(self, player):
		if player.vel.magnitude() < 1:
			return Idle()

	def update(self, dt, player):
		player.animate(f'run_{player.get_direction()}', 15 * dt)
		player.input()
		player.physics(dt)


class Player(NPC):
	def __init__(self, game, scene, groups, pos, z, name):
		super().__init__(game, scene, groups, pos, z, name)

		self.state = Idle()
		self.get_initial_direction()

	def get_initial_direction(self):
		#move the player slightly in the relevant direction of where they enter the room
		scene_size = self.scene.camera.get_scene_size(self.scene)
		if self.pos.x < TILESIZE * 4: self.vel.x = 1
		elif self.pos.x > scene_size[0] - TILESIZE * 4: self.vel.x = -1
		elif self.pos.y > scene_size[1]/2: self.vel.y = -1
		else: self.vel.y = 1

	def input(self):

		if INPUTS['left']: self.move['left'] = True
		elif INPUTS['right']: self.move['right'] = True
		else: self.move['left'], self.move['right'] = False, False

		if INPUTS['up']: self.move['up'] = True
		elif INPUTS['down']: self.move['down'] = True
		else: self.move['up'], self.move['down'] = False, False
