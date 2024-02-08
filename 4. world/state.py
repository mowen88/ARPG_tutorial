import pygame
from settings import *
from characters import Player
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
		if len(self.game.states) > 1:
			self.prev_state = self.game.states[-1]
		self.game.states.append(self)

	def exit_state(self):
		self.game.states.pop()

# class Object(pygame.sprite.Sprite):
# 	def __init__(self, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z= LAYERS['blocks']):
# 		super().__init__(groups)

# 		self.image = surf
# 		self.rect = self.image.get_rect(topleft = pos)
# 		self.hitbox = self.rect.copy().inflate(0,0)
# 		self.old_hitbox = self.hitbox.copy()
# 		self.z = z

# class AnimatedObject(pygame.sprite.Sprite):
# 	def __init__(self, game, groups, pos, path, z):
# 		super().__init__(groups)

# 		self.game = game
# 		self.frames = self.game.get_images(path)
# 		self.frame_index = 0
# 		self.image = self.frames[self.frame_index]
# 		self.rect = self.image.get_rect(topleft = pos)
# 		self.hitbox = self.rect.copy().inflate(0,0)
# 		self.old_hitbox = self.hitbox.copy()
# 		self.z = z

# 	def animate(self, animation_speed, loop=True):
# 		self.frame_index += animation_speed
# 		self.frame_index = len(self.frames)-1 if not loop else self.frame_index % len(self.frames)
# 		self.image = self.frames[int(self.frame_index)]

# 	def update(self, dt):
# 		self.animate(15 * dt)

class Camera(pygame.sprite.Group):
    def __init__(self, game, scene):
        super().__init__()

        self.game = game
        self.scene = scene
        self.offset = pygame.math.Vector2()

    def update(self, dt):
    	pass

    def draw(self, screen, target, group):
        screen.fill(COLOURS['red'])

        self.offset.x = target.rect.centerx - WIDTH/2
        self.offset.y = target.rect.centery - HEIGHT/2

        for layer in LAYERS.values():
            for sprite in group:
                if sprite.z == layer: # and self.scene.visible_window.contains(sprite.rect):
                    offset = sprite.rect.topleft - self.offset
                    self.game.screen.blit(sprite.image, offset)

class Scene(State):
	def __init__(self, game):
		State.__init__(self, game)

		self.game = game
		
		self.camera = Camera(self.game, self)
		self.drawn_sprites = pygame.sprite.Group()
		self.update_sprites = pygame.sprite.Group()

		self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (100,100), 'player', LAYERS['player'])

	def update(self, dt):
		self.update_sprites.update(dt)

	def debug(self, debug_list):
		for index, name in enumerate(debug_list):
			self.game.render_text(name, COLOURS['white'], self.game.font, (10, 15 * index), False)

	def draw(self, screen):

		self.camera.draw(screen, self.player, self.drawn_sprites)
		self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
					str('vel: ' + str(round(self.player.vel.x, 2) + round(self.player.vel.y, 2))),
					None,])

class SplashScreen(State):
	def __init__(self, game):
		State.__init__(self, game)
		
	def update(self, dt):
		if INPUTS['space']:
			Scene(self.game).enter_state()
			self.game.reset_inputs()

	def draw(self, screen):
		screen.fill(COLOURS['blue'])
