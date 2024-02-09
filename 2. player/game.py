import pygame, sys, os
from state import SplashScreen
from settings import *

class Game:
    def __init__(self):
        pygame.init()
      
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN|pygame.SCALED)
        self.font = pygame.font.Font(FONT, TILESIZE) #int(TILESIZE))
        self.running = True
        #initialise first state and state stack
        self.states = []
        self.splash_screen = SplashScreen(self)
        self.states.append(self.splash_screen)
 
    def render_text(self, text, colour, font, pos, centralised=True):
        surf = font.render (str(text), False, colour)
        rect = surf.get_rect(center = pos) if centralised else surf.get_rect(topleft = pos)
        self.screen.blit(surf, rect)

        def get_inputs(self):
        # mapping inputs to INPUTS dictionary in global settings file, so they return true when key is pressed and false on key up.
        # this allows easy access to all keys using the global INPUTS dictionary
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    INPUTS['escape'] = True
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    INPUTS['space'] = True
                elif event.key == (pygame.K_LEFT or pygame.K_a):
                    INPUTS['left'] = True
                elif event.key == (pygame.K_RIGHT or pygame.K_d):
                    INPUTS['right'] = True
                elif event.key == (pygame.K_UP or pygame.K_w):
                    INPUTS['up'] = True
                elif event.key == (pygame.K_DOWN or pygame.K_s):
                    INPUTS['down'] = True
               
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_SPACE:
                    INPUTS['space'] = False 
                elif event.key == (pygame.K_LEFT or pygame.K_a):
                    INPUTS['left'] = False
                elif event.key == (pygame.K_RIGHT or pygame.K_d):
                    INPUTS['right'] = False
                elif event.key == (pygame.K_UP or pygame.K_w):
                    INPUTS['up'] = False
                elif event.key == (pygame.K_DOWN or pygame.K_s):
                    INPUTS['down'] = False

            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    INPUTS['scroll_up'] = True
                elif event.y == -1:
                    INPUTS['scroll_down'] = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    INPUTS['left_click'] = True
                elif event.button == 3:
                    INPUTS['right_click'] = True
                elif event.button == 4:
                    INPUTS['scroll_down'] = True
                elif event.button == 2:
                    INPUTS['scroll_up'] = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    INPUTS['left_click'] = False
                elif event.button == 3:
                    INPUTS['right_click'] = False
                elif event.button == 4:
                    INPUTS['scroll_down'] = False
                elif event.button == 2:
                    INPUTS['scroll_up'] = False

    def reset_inputs(self):
        # a function that can be called to reset all inputs to false
        for key in INPUTS:
            INPUTS[key] = False

    def loop(self):
        while self.running:
            dt = self.clock.tick()/1000
            self.get_inputs()
            self.states[-1].update(dt)
            self.states[-1].draw(self.screen)
            pygame.display.flip()
        
if __name__ == "__main__":
    game = Game()
    game.loop()