import pygame
from settings import *
from characters import Player

class State:
	def __init__(self, game):
		self.game = game
		self.prev_state = None

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

# class Camera(pygame.sprite.Group):
#     def __init__(self, game, scene):
#         super().__init__()

#         self.game = game
#         self.scene = scene
#         self.offset = pygame.math.Vector2()

#     def update(self, dt):
#     	pass

#     def draw(self, screen, target, group):
#         screen.fill(COLOURS['light green'])

#         self.offset.x = target.rect.centerx - WIDTH/2
#         self.offset.y = target.rect.centery - HEIGHT/2

#         for layer in LAYERS.values():
#             for sprite in group:
#                 if sprite.z == layer: # and self.scene.visible_window.contains(sprite.rect):
#                     offset = sprite.rect.topleft - self.offset
#                     self.game.screen.blit(sprite.image, offset)

class Scene(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		
		# self.camera = Camera(self.game, self)
		self.drawn_sprites = pygame.sprite.Group()
		self.update_sprites = pygame.sprite.Group()

		self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (100,100), 'player')

	def update(self, dt):
		self.update_sprites.update(dt)

	def debug(self, debug_list):
		for index, name in enumerate(debug_list):
			self.game.render_text(name, COLOURS['white'], self.game.font, (10, 15 * index), False)

	def draw(self, screen):
		screen.fill(COLOURS['light green'])
		self.drawn_sprites.draw(screen)
		#self.camera.draw(screen, self.player, self.drawn_sprites)
		self.debug([
					str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
					str('vel x: ' + str(round(self.player.vel.x, 2))),
					str('vel y: ' + str(round(self.player.vel.y, 2)))
					])