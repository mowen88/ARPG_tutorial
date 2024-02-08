import pygame
from settings import *

class State:
	def __init__(self, game):
		self.game = game
		self.prev_state = None

	def actions(self, events):
		pass

	def update(self, dt):
		pass

	def draw(self, screen):
		pass

	def enter_state(self):
		if len(self.game.states) > 1:
			self.prev_state = self.game.states[-1]
		self.game.states.append(self)

	def exit_state(self):
		self.game.states.pop()

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
		self.drawn_sprites = pygame.sprite.Group()
		self.update_sprites = pygame.sprite.Group()

	def debug(self, debug_list):
		for index, name in enumerate(debug_list):
			self.game.render_text(name, COLOURS['white'], self.game.font, (10, 15 * index), False)

	def update(self, dt):
		self.update_sprites.update(dt)
		if INPUTS['space']:
			self.exit_state()
			self.game.reset_inputs()

	def draw(self, screen):
		screen.fill(COLOURS['red'])
		self.drawn_sprites.draw(screen)
		self.debug([
					str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
					str('variable: '+ 'value'),
					])

