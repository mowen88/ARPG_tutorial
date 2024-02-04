import pygame, sys, os
from state import SplashScreen
from settings import *

class Game:
    def __init__(self):
        pygame.init()
      
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((RES), pygame.FULLSCREEN|pygame.SCALED)
        self.font = pygame.font.Font(FONT, TILESIZE) #int(TILESIZE))
        self.running = True
        #initialise first state and state stack
        self.stack = []
        self.splash_screen = SplashScreen(self)
        self.stack.append(self.splash_screen)

    def get_events(self):
    	# mapping inputs to ACTIONS dictionary in global settings file, so they return true when key is pressed and false on key up.
    	# this allows easy access to all keys using the global ACTIONS dictionary
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ACTIONS['escape'] = True
                    self.running = False
                elif event.key == pygame.K_e:
                    ACTIONS['e'] = True
                elif event.key == pygame.K_z:
                    ACTIONS['z'] = True
                elif event.key == pygame.K_x:
                    ACTIONS['x'] = True
                elif event.key == pygame.K_c:
                    ACTIONS['c'] = True
                elif event.key == pygame.K_TAB:
                    ACTIONS['tab'] = True
                elif event.key == pygame.K_SPACE:
                    ACTIONS['space'] = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    ACTIONS['left'] = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    ACTIONS['right'] = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    ACTIONS['up'] = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    ACTIONS['down'] = True

               
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    ACTIONS['e'] = False
                elif event.key == pygame.K_z:
                    ACTIONS['z'] = False
                elif event.key == pygame.K_x:
                    ACTIONS['x'] = False
                elif event.key == pygame.K_c:
                    ACTIONS['c'] = False
                elif event.key == pygame.K_TAB:
                    ACTIONS['tab'] = False
                elif event.key == pygame.K_SPACE:
                    ACTIONS['space'] = False 
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    ACTIONS['left'] = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    ACTIONS['right'] = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    ACTIONS['up'] = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    ACTIONS['down'] = False

            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    ACTIONS['scroll_up'] = True
                elif event.y == -1:
                    ACTIONS['scroll_down'] = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    ACTIONS['left_click'] = True
                elif event.button == 3:
                    ACTIONS['right_click'] = True
                elif event.button == 4:
                    ACTIONS['scroll_down'] = True
                elif event.button == 2:
                    ACTIONS['scroll_up'] = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    ACTIONS['left_click'] = False
                elif event.button == 3:
                    ACTIONS['right_click'] = False
                elif event.button == 4:
                    ACTIONS['scroll_down'] = False
                elif event.button == 2:
                    ACTIONS['scroll_up'] = False

    def reset_keys(self):
    	# a function that can bel called to reset all inputs to false
        for action in ACTIONS:
            ACTIONS[action] = False

    def get_animation_states(self, path):
        file_dict = {}
        for file_name in os.listdir(path):
            file_dict.update({file_name:[]})
        return file_dict

    def get_images(self, path):
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            img = pygame.image.load(full_path).convert_alpha()
            images.append(img)
        return images
 
    def render_text(self, text, colour, font, pos):
        surf = font.render (str(text), False, colour)
        rect = surf.get_rect(topleft = pos)
        self.screen.blit(surf, rect)

    def actions(self):
        self.stack[-1].actions(self.get_events)

    def update(self, dt):
        self.stack[-1].update(dt)
 
    def draw(self, screen):
        self.stack[-1].draw(screen)
        #self.custom_cursor(screen)
        pygame.display.flip()

    def main_loop(self):
        dt = self.clock.tick(60)/1000
        self.get_events()
        self.update(dt)
        self.draw(self.screen)
        
if __name__ == "__main__":
    game = Game()
    while game.running:
        game.main_loop()
       

