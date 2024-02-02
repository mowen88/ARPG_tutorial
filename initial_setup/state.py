from settings import *
import pygame
from pytmx.util_pygame import load_pygame

class State():
	def __init__(self, game):
		self.game = game
		self.prev_state = None

	def update(self, dt):
		pass

	def draw(self, screen):
		pass

	def enter_state(self):
		if len(self.game.stack) > 1:
			self.prev_state = self.game.stack[-1]
		self.game.stack.append(self)

	def exit_state(self):
		self.game.stack.pop()

class Tile(pygame.sprite.Sprite):
	def __init__(self, groups, pos, surf=pygame.Surface((TILESIZE, TILESIZE)), z= LAYERS['blocks']):
		super().__init__(groups)

		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.copy().inflate(0,0)
		self.old_hitbox = self.hitbox.copy()
		self.z = z

class AnimatedObject(pygame.sprite.Sprite):
	def __init__(self, game, groups, pos, name, z= LAYERS['blocks']):
		super().__init__(groups)

		self.game = game
		self.frame_index = 0
		self.frames = self.game.get_images(name)

	def animate(self, animation_speed):
		self.frame_index += animation_speed
		self.frame_index = self.frame_index % len(self.frames)

	def update(self, dt):
		self.animate(0.25 * dt)

class Entity(AnimatedObject):
	def __init__(self, game, scene, groups, pos, name, z):
		super().__init__(game, groups, pos, name, z)

		self.scene = scene
		self.name = name
		self.z = z

class NPC(Entity):
	def __init__(self, game, scene, groups, pos, path, z):
		super().__init__(game, groups, pos, z)

		self.image = self.animations['fall'][self.frame_index].convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5,- self.rect.height * 0.5)
		self.old_pos = self.pos.copy()
		self.old_hitbox = self.hitbox.copy()
		self.alive = True
		
		self.import_images()

	def import_images(self):
		path = f'assets/characters/{self.name}/'

		self.animations = self.game.get_animation_states(path)

		for animation in self.animations.keys():
			full_path = path + animation
			self.animations[animation] = self.game.get_images(full_path)



class Player(NPC):
	def __init__(self, game, scene, groups, pos, name, z):
		super().__init__(game, scene, groups, pos, name, z)

		self.import_images()


	def animate(self, state, speed, loop=True):

		self.frame_index += speed

		if self.frame_index >= len(self.animations[state]):
			if loop: 
				self.frame_index = 0
			else:
				self.frame_index = len(self.animations[state]) -1
		
		direction = self.facing if self.facing == 1 else 0
		self.image = pygame.transform.flip(self.animations[state][int(self.frame_index)], direction-1, False)

	def physics_x(self, dt):
			
		self.acc.x += self.vel.x * self.fric
		self.vel.x += self.acc.x * dt

		if self.platform: 
			if self.hitbox.right < self.platform.hitbox.left or self.hitbox.left > self.platform.hitbox.right:
				self.platform = None
			elif self.platform.vel.x != 0:
				self.pos.x = round(self.platform.pos.x) +round(self.relative_position.x)

		self.pos.x += self.vel.x * dt + (0.5 * self.acc.x) * dt

		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx

class Scene(State):
	def __init__(self, game):
		State.__init__(self, game)
		
		self.drawn_sprites = pygame.sprite.Group()
		self.update_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()

		self.player = Player(self.game, self, [self.drawn_sprites, self.update_sprites], (100,100), 'player', LAYERS['player'])

	def debug(self, debug_list):
		for index, name in enumerate(debug_list):
			self.game.render_text(name, WHITE, self.game.font, (10, 15 * index))

	def update(self, dt):
		self.update_sprites.update(dt)

	def draw(self, screen):
		screen.fill(RED)
		self.drawn_sprites.draw(screen)

		self.debug([str('FPS: '+ str(round(self.game.clock.get_fps(), 2))),
					None,])


class SplashScreen(State):
	def __init__(self, game):
		State.__init__(self, game)
		
	def update(self, dt):
		if ACTIONS['space']:
			Scene(self.game).enter_state()

	def draw(self, screen):
		screen.fill(BLUE)
