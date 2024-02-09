import pygame
from settings import *
from camera import Camera
from characters import Player
from objects import Object
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
			Scene(self.game).enter_state()
			self.game.reset_inputs()

	def draw(self, screen):
		screen.fill(COLOURS['blue'])
		self.game.render_text('Press space', COLOURS['white'], self.game.font, (WIDTH/2, HEIGHT/2))

class Scene(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		
		self.camera = Camera(self)
		self.drawn_sprites = pygame.sprite.Group()
		self.update_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()

		# create all objects in the scene using tmx data
		self.tmx_data = load_pygame(f'scenes/0/0.tmx')
		self.create_scene()

	def create_scene(self):

		layers = []
		for layer in self.tmx_data.layers:
			layers.append(layer.name)

		if 'blocks' in layers:
			for x, y, surf in self.tmx_data.get_layer_by_name('blocks').tiles():
				#tile_id = self.tmx_data.get_tile_gid(x,y,0)
				Object([self.block_sprites, self.drawn_sprites], (x * TILESIZE, y * TILESIZE), 'blocks', surf)

		if 'entries' in layers:
			for obj in self.tmx_data.get_layer_by_name('entries'):
				if obj.name == '0':
					self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'characters', 'player')
					self.target = self.player

	def update(self, dt):
		self.update_sprites.update(dt)
		self.camera.update(dt, self.target)

	def debug(self, debug_list):
		for index, name in enumerate(debug_list):
			self.game.render_text(name, COLOURS['white'], self.game.font, (10, 15 * index), False)

	def draw(self, screen):
		self.camera.draw(screen, self.drawn_sprites)
		self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
					str('vel x: ' + str(round(self.player.vel.x, 2))),
					str('vel y: ' + str(round(self.player.vel.y, 2)))
					])
