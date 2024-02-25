import pygame
from settings import *
from camera import Camera
from transition import Transition
from characters import NPC
from player import Player
from objects import Collider, Object, Wall
from pytmx.util_pygame import load_pygame

class State:
	def __init__(self, game):
		self.game = game
		self.prev_state = None

	def enter_state(self):
		if len(self.game.states) > 1:
			self.prev_state = self.game.states[-1]
		self.game.states.append(self)

	def exit_state(self):
		self.game.states.pop()

	def update(self, dt):
		pass

	def draw(self, screen):
		pass

class SplashScreen(State):
	def __init__(self, game):
		State.__init__(self, game)

	def update(self, dt):
		if INPUTS['space']:
			Scene(self.game, '0', '0').enter_state()
			self.game.reset_inputs()

	def draw(self, screen):
		screen.fill(COLOURS['blue'])
		self.game.render_text('Splash screen, press space', COLOURS['white'], self.game.font, (WIDTH/2, HEIGHT/2))

class Scene(State):
	def __init__(self, game, current_scene, entry_point):
		State.__init__(self, game)

		self.current_scene = current_scene
		self.entry_point = entry_point

		self.camera = Camera(self)
		self.update_sprites = pygame.sprite.Group()
		self.drawn_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		self.exit_sprites = pygame.sprite.Group()
		self.platform_sprites = pygame.sprite.Group()

		self.tmx_data = load_pygame(f'scenes/{self.current_scene}/{self.current_scene}.tmx')
		self.create_scene()

		self.transition = Transition(self)
		self.camera.offset = vec(self.player.rect.centerx - WIDTH/2, self.player.rect.centery - HEIGHT/2)

	def go_to_scene(self):
		Scene(self.game, self.new_scene, self.entry_point).enter_state()

	def create_scene(self):
		layers = []
		for layer in self.tmx_data.layers:
			layers.append(layer.name)

		if 'blocks' in layers:
			for x, y, surf in self.tmx_data.get_layer_by_name('blocks').tiles():
				Wall([self.block_sprites, self.drawn_sprites], (x * TILESIZE, y * TILESIZE), 'blocks', surf)

		if 'entries' in layers:
			for obj in self.tmx_data.get_layer_by_name('entries'):
				if obj.name == self.entry_point:
					self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'blocks', 'player')
					self.target = self.player

		if 'exits' in layers:
			for obj in self.tmx_data.get_layer_by_name('exits'):
				Collider([self.exit_sprites], (obj.x, obj.y), (obj.width, obj.height), obj.name)

		if 'platforms' in layers:
			for obj in self.tmx_data.get_layer_by_name('platforms'):
				Object([self.platform_sprites, self.drawn_sprites], (obj.x, obj.y), 'floor', obj.image)

		if 'entities' in layers:
			for obj in self.tmx_data.get_layer_by_name('entities'):
				if obj.name == 'npc':
					self.npc = NPC(self.game, self, [self.update_sprites, self.drawn_sprites], (obj.x, obj.y), 'blocks', 'npc')

	def debugger(self, debug_list):
		for index, name in enumerate(debug_list):
			self.game.render_text(name, COLOURS['white'], self.game.font, (10, 15 * index), False)

	def update(self, dt):
		self.update_sprites.update(dt)
		self.camera.update(dt, self.target)
		self.transition.update(dt)

	def draw(self, screen):
		self.camera.draw(screen, self.drawn_sprites)
		self.transition.draw(screen)
		self.debugger([
						str('FPS: ' + str(round(self.game.clock.get_fps(), 2))),
						str('vel: ' + str(self.player.state)),
						str('state: ' + str(self.player.rect))
			])




		