import pygame
from settings import *
from transition import Transition
from camera import Camera
from characters import NPC
from player import Player
from objects import Collider, Object, Wall
from pytmx.util_pygame import load_pygame

class State:
	def __init__(self, game):
		self.game = game
		self.prev_state = None

	def update(self, dt):
		pass

	def draw(self, screen):
		pass

	def enter_state(self):
		
		self.prev_state = self.game.prev_state
		self.game.state = self

	def exit_state(self):
		self.game.state = self.prev_state

class SplashScreen(State):
	def __init__(self, game):
		State.__init__(self, game)
		
	def update(self, dt):
		if INPUTS['space']:
			Scene(self.game, '0', '0').enter_state()
			self.game.reset_inputs()

	def draw(self, screen):
		screen.fill(COLOURS['blue'])
		self.game.render_text('Press space', COLOURS['white'], self.game.font, (WIDTH/2, HEIGHT/2))

class Scene(State):
	def __init__(self, game, current_scene, entry_point):
		State.__init__(self, game)

		self.game = game
		self.current_scene = current_scene
		self.entry_point = entry_point

		self.camera = Camera(self)
		self.drawn_sprites = pygame.sprite.Group()
		self.update_sprites = pygame.sprite.Group()
		self.exit_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()

		
		# create all objects in the scene using tmx data
		self.tmx_data = load_pygame(f'scenes/{self.current_scene}/{self.current_scene}.tmx')
		self.create_scene()

		self.transition = Transition(self)

	def go_to_scene(self):
		Scene(self.game, self.new_scene, self.entry_point).enter_state()

	def create_scene(self):
		layers = []
		for layer in self.tmx_data.layers:
			layers.append(layer.name)

		if 'blocks' in layers:
			for x, y, surf in self.tmx_data.get_layer_by_name('blocks').tiles():
				#tile_id = self.tmx_data.get_tile_gid(x,y,0)
				Wall([self.block_sprites, self.drawn_sprites], (x * TILESIZE, y * TILESIZE), 'blocks', surf)

		if 'entries' in layers:
			for obj in self.tmx_data.get_layer_by_name('entries'):
				if obj.name == self.entry_point:
					self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'blocks', 'player')
					self.target = self.player

		if 'exits' in layers:
			for obj in self.tmx_data.get_layer_by_name('exits'):
				Collider([self.exit_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)

		if 'entities' in layers:
			for obj in self.tmx_data.get_layer_by_name('entities'):
				if obj.name == 'npc':
					self.npc = NPC(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'blocks', 'player')

	def update(self, dt):
		self.update_sprites.update(dt)
		self.transition.update(dt)
		
	def debug(self, debug_list):
		for index, name in enumerate(debug_list):
			self.game.render_text(name, COLOURS['white'], self.game.font, (10, 15 * index), False)

	def draw(self, screen):
		self.camera.draw(screen, self.target, self.drawn_sprites)
		self.transition.draw(screen)
		self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
					str('vel x: ' + str(round(self.player.vel.x, 2))),
					str('vel y: ' + str(round(self.player.vel.y, 2))),
					str('state: ' + str(self.player.state)),
					])

