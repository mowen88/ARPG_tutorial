
TILESIZE = 16

FONT = 'assets/homespun.ttf'

WIDTH, HEIGHT = 400,224 #(384, 216)#(512, 288)#(320, 180)#(480, 270)#(640, 360)#(960, 540)#(512, 288)

INPUTS = {'escape':False, 'space':False,'up':False, 'down':False, 'left':False, 'right':False, 'e':False,
			'tab':False, 'left_click':False, 'right_click':False, 'scroll_up':False, 'scroll_down':False, 'r':False}
			
COLOURS = {'black':(0,0,0), 'white':(255,255,255), 'red':(255,0,0), 'green':(0,255,0),'blue':(0,0,255), 'light green':(99,196,141)}

LAYERS = ['background',
		  'objects',
		  'characters',
		  'particles',
		  'blocks',
		  'foreground']
