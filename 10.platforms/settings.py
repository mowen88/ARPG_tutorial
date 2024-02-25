from pygame.math import Vector2 as vec

WIDTH, HEIGHT = 400, 224
TILESIZE = 16
FONT = 'assets/homespun.ttf'

INPUTS = {'escape': False, 'space': False, 'up': False, 'down': False, 'left': False, 'right': False, 
			'left_click': False, 'right_click': False, 'scroll_up': False, 'scroll_down': False,}

COLOURS = {'black':(0,0,0), 'white':(255,255,255), 'red':(200,100,100), 'green':(100,200,100),'blue':(100,100,200)}

LAYERS = ['background', 
		  'floor',
		  'objects',
		  'characters',
		  'blocks', 
		  'particles',
		  'foreground']

SCENE_DATA = {
			  0:{1:1, 3:2},
			  1:{1:0, 2:2},
			  2:{2:1, 3:0}
			 }