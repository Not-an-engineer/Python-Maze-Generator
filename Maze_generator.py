import pygame
from pygame.locals import *
import pygame_gui
import numpy as np
import random
from random import shuffle
import time
import math
import sys
import pygame.freetype

sys.setrecursionlimit(5000)  # Increase number as needed for your maze size


# X by Y for size
maze_resolution = (40,40)
# windows size
window_size = (400,400)


maze_array = np.zeros(maze_resolution, dtype=np.int64)

N,E,S,W = 1,2,4,8
DX = {
	E : 1,
	W :-1,
	N : 0,
	S : 0 
}
DY = {
	E : 0,
	W : 0,
	N : -1,
	S : 1 
}
directions = [N,E,S,W]
opposite = {
	N : S,
	S : N,
	E : W,
	W : E
}

order = []

top_window_padding = 7
bottom_window_padding = 100
left_window_padding = 7
right_window_padding = 7


pygame.init()
window = pygame.display.set_mode((window_size[0]+right_window_padding+left_window_padding,window_size[1]+bottom_window_padding+top_window_padding), pygame.RESIZABLE)
#window = pygame.display.set_mode(pygame.NOFRAME)
window.fill((0,0,0))


my_font = pygame.font.SysFont('Comic Sans MS', 18)


manager = pygame_gui.UIManager((window_size[0]+right_window_padding+left_window_padding,window_size[1]+bottom_window_padding+top_window_padding))
clock = pygame.time.Clock()


# total_grid = []
# for i in range(maze_resolution[0]):
# 	for j in range(maze_resolution[1]):
# 		total_grid.append((i,j))

# for i,j in total_grid:
# 	pygame.draw.rect(window, (100,100,100), [i*(window_size[0]/maze_resolution[0])+left_window_padding,j*(window_size[1]/maze_resolution[1])+top_window_padding,window_size[0]/maze_resolution[0],window_size[1]/maze_resolution[1]], width=1)

# pygame.draw.line(window, wall_color, (x*(window_size[0]/maze_resolution[0]),y*(window_size[1]/maze_resolution[1])), (x*(window_size[0]/maze_resolution[0])+(window_size[0]/maze_resolution[0]),y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])), width=1)

def draw_maze(window, wall_color=(100,100,100), prints=True, delay=2):
	window.fill((0,0,0))

	if prints: print(" " + "_" * (maze_resolution[0] * 2 - 1))
	pygame.draw.line(window, wall_color, (left_window_padding,top_window_padding), (window_size[0]+left_window_padding,(top_window_padding)), width=1)

	for y in range(maze_resolution[1]):
		if prints: print("|", end="")
		pygame.draw.line(window, wall_color, ((left_window_padding),y*(window_size[1]/maze_resolution[1])+top_window_padding), (left_window_padding,y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), width=1)

		for x in range(maze_resolution[0]):

			# South wall
			if prints: print(" " if (maze_array[x, y] & S) != 0 else "_", end="")
			if (maze_array[x, y] & S) != 0:
				pass
			else:
				pygame.draw.line(window, wall_color, (x*(window_size[0]/maze_resolution[0])+left_window_padding,y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), (x*(window_size[0]/maze_resolution[0])+(window_size[0]/maze_resolution[0])+(left_window_padding),y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), width=1)

			# East wall
			if (maze_array[x, y] & E) != 0:

				# Avoid out-of-bounds on right edge
				if x < maze_resolution[0] - 1:
					south_open = ((maze_array[x, y] | maze_array[x + 1, y]) & S) != 0
					if prints: print(" " if south_open else "_", end="")
					if south_open:
						pass
					else:
						pygame.draw.line(window, wall_color, (x*(window_size[0]/maze_resolution[0])+(left_window_padding),y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), (x*(window_size[0]/maze_resolution[0])+(window_size[0]/maze_resolution[0])+(right_window_padding),y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), width=1)

				else:
					if prints: print(" ", end="")
			else:
				if prints: print("|", end="")
				pygame.draw.line(window, wall_color, (x*(window_size[0]/maze_resolution[0])+(window_size[0]/maze_resolution[0])+(left_window_padding),y*(window_size[1]/maze_resolution[1])+(top_window_padding)), (x*(window_size[0]/maze_resolution[0])+(window_size[0]/maze_resolution[0])+(left_window_padding),y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), width=1)
				
				manager.draw_ui(window)
				pygame.display.flip()
				time.sleep(delay/1000)


		if prints: print()
	pass


def draw_maze_order(window, wall_color=(100,100,100), prints=True, delay=2):
	global order
	#window.fill((0,0,0))

	if prints: print(" " + "_" * (maze_resolution[0] * 2 - 1))
	pygame.draw.line(window, wall_color, (left_window_padding,top_window_padding), (window_size[0]+left_window_padding,(top_window_padding)), width=1)

	for c,(x,y) in enumerate(order):
		offset = 0
		#pygame.draw.rect(window, (0,0,0), [x*(window_size[0]/maze_resolution[0])+left_window_padding+offset,y*(window_size[1]/maze_resolution[1])+top_window_padding+offset,window_size[0]/maze_resolution[0],window_size[1]/maze_resolution[1]], width=0)
		offset = 2
		#pygame.draw.rect(window, (200,0,0), [x*(window_size[0]/maze_resolution[0])+left_window_padding+offset,y*(window_size[1]/maze_resolution[1])+top_window_padding+offset,window_size[0]/maze_resolution[0]-offset*2,window_size[1]/maze_resolution[1]-offset*2], width=0)
		if prints: print("|", end="")
		pygame.draw.line(window, wall_color, ((left_window_padding),y*(window_size[1]/maze_resolution[1])+top_window_padding), (left_window_padding,y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), width=1)

		

		# South wall
		if prints: print(" " if (maze_array[x, y] & S) != 0 else "_", end="")
		if (maze_array[x, y] & S) != 0:
			pass
		else:
			pygame.draw.line(window, wall_color, (x*(window_size[0]/maze_resolution[0])+left_window_padding,y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), (x*(window_size[0]/maze_resolution[0])+(window_size[0]/maze_resolution[0])+(left_window_padding),y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), width=1)

		# East wall
		if (maze_array[x, y] & E) != 0:

			# Avoid out-of-bounds on right edge
			if x < maze_resolution[0] - 1:
				south_open = ((maze_array[x, y] | maze_array[x + 1, y]) & S) != 0
				if prints: print(" " if south_open else "_", end="")
				if south_open:
					pass
				else:
					pygame.draw.line(window, wall_color, (x*(window_size[0]/maze_resolution[0])+(left_window_padding),y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), (x*(window_size[0]/maze_resolution[0])+(window_size[0]/maze_resolution[0])+(right_window_padding),y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), width=1)

			else:
				if prints: print(" ", end="")
		else:
			if prints: print("|", end="")
			pygame.draw.line(window, wall_color, (x*(window_size[0]/maze_resolution[0])+(window_size[0]/maze_resolution[0])+(left_window_padding),y*(window_size[1]/maze_resolution[1])+(top_window_padding)), (x*(window_size[0]/maze_resolution[0])+(window_size[0]/maze_resolution[0])+(left_window_padding),y*(window_size[1]/maze_resolution[1])+(window_size[1]/maze_resolution[1])+(top_window_padding)), width=1)
			
			manager.draw_ui(window)
			pygame.display.flip()
			gui_manager()
			time.sleep(delay/1000)


		if prints: print()
	pass

def carve_passage(cx, cy, maze):
	global order

	shuffle(directions)

	for d in directions:
		nx,ny = cx + DX[d], cy + DY[d]

		if 0 <= nx <= np.shape(maze)[0]-1 and 0 <= ny <= np.shape(maze)[1]-1 and maze[nx,ny] == 0:
			maze[cx,cy] |= d
			maze[nx,ny] |= opposite[d]
			order.append((nx,ny))
			carve_passage(nx,ny,maze)
	pass

amount_of_buttons = 4
spacing = (window_size[0]/amount_of_buttons)

top_button_reset_padding = 0
bottom_button_reset_padding = 0
left_button_reset_padding = 0
right_button_reset_padding = 0

reset = pygame_gui.elements.UIButton(
	relative_rect=pygame.Rect((left_window_padding+left_button_reset_padding-2+((spacing-((0.05*window_size[0])+40))/2),window_size[1]+top_window_padding+top_button_reset_padding),(((0.05*window_size[0])+40-right_button_reset_padding),((0.05*window_size[0])+20-bottom_button_reset_padding))),
	text='Reset',
	manager=manager
)



run = pygame_gui.elements.UIButton(
	relative_rect=pygame.Rect((spacing,0), (((0.05*window_size[0])+40),((0.05*window_size[0])+20))),
	text='Run',
	manager=manager,
	anchors={'bottom': 'bottom',
			 'right': 'right',
			 'bottom_target': reset,
			 'right_target': reset}
)



set_size_x = pygame_gui.elements.UITextEntryLine(
	relative_rect=pygame.Rect((spacing-15,0), (((0.05*window_size[0])+40)/2,((0.05*window_size[0])+20))),
	manager=manager,
	anchors={'bottom': 'bottom',
			 'right': 'right',
			 'bottom_target': run,
			 'right_target': run}
)



set_size_y = pygame_gui.elements.UITextEntryLine(
	relative_rect=pygame.Rect((spacing+10+((0.05*window_size[0])+40)/2,0), (((0.05*window_size[0])+40)/2,((0.05*window_size[0])+20))),
	manager=manager,
	anchors={'bottom': 'bottom',
			 'right': 'right',
			 'bottom_target': run,
			 'right_target': run}
)



set_res_x = pygame_gui.elements.UITextEntryLine(
	relative_rect=pygame.Rect((spacing-15,0), (((0.05*window_size[0])+40)/2,((0.05*window_size[0])+20))),
	manager=manager,
	anchors={'bottom': 'bottom',
			 'right': 'right',
			 'bottom_target': set_size_x,
			 'right_target': set_size_x}
)



set_res_y = pygame_gui.elements.UITextEntryLine(
	relative_rect=pygame.Rect((spacing+10+((0.05*window_size[0])+40)/2,0), (((0.05*window_size[0])+40)/2,((0.05*window_size[0])+20))),
	manager=manager,
	anchors={'bottom': 'bottom',
			 'right': 'right',
			 'bottom_target': set_size_x,
			 'right_target': set_size_x}
)


def gui_manager():
	global window
	global maze_resolution
	global maze_array
	global window_size
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()

		# if event.type == pygame.MOUSEBUTTONUP:
		# 	pos = pygame.mouse.get_pos()
		# 	print(pos)

		manager.process_events(event)

		if event.type == pygame_gui.UI_BUTTON_PRESSED:
			if event.ui_element == reset:
				print('RESET')
				# maze_array = np.zeros(maze_resolution, dtype=np.int64)
				carve_passage(0,0,maze_array)
				# window.fill((0,0,0))


		if event.type == pygame_gui.UI_BUTTON_PRESSED:
			if event.ui_element == run:
				print('RUN')
				#window.fill((0,0,0))
				draw_maze(window, wall_color=(100,100,100), prints=False, delay=0)

		if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
			if event.ui_element == set_size_x:
				print('SET SIZE X')
				maze_resolution = (int(event.text),np.size(maze_array,0))
				maze_array = np.zeros(maze_resolution, dtype=np.int64)

		if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
			if event.ui_element == set_size_y:
				print('SET SIZE Y')
				maze_resolution = (np.size(maze_array,1),int(event.text))
				maze_array = np.zeros(maze_resolution, dtype=np.int64)

		if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
			if event.ui_element == set_res_x:
				print('SET RESOLUTION X')
				x,y = window_size
				window_size = (int(event.text),y)
				window = pygame.display.set_mode((window_size[0]+right_window_padding+left_window_padding,window_size[1]+bottom_window_padding+top_window_padding), pygame.RESIZABLE)

		if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
			if event.ui_element == set_res_y:
				print('SET RESOLUTION Y')
				x,y = window_size
				window_size = (x,int(event.text))
				window = pygame.display.set_mode((window_size[0]+right_window_padding+left_window_padding,window_size[1]+bottom_window_padding+top_window_padding), pygame.RESIZABLE)

def text():
	text_surface = my_font.render("X", False, (255,255,255))
	window.blit(text_surface, (set_size_x.rect.topright[0]+5, window_size[1]+15))

	text_surface2 = my_font.render("Maze Size", False, (255,255,255))
	window.blit(text_surface2, ((set_size_x.rect.topright[0]+2)-(set_size_x.rect.topright[0]+2)/(amount_of_buttons+2), window_size[1]+((0.05*window_size[0])+20)))

	text_surface3 = my_font.render("X", False, (255,255,255))
	window.blit(text_surface3, (set_res_x.rect.topright[0]+5, window_size[1]+15))

	text_surface4 = my_font.render("Maze Res", False, (255,255,255))
	window.blit(text_surface4, ((set_res_x.rect.topright[0]+30)-(set_res_x.rect.topright[0]+2)/(amount_of_buttons+2), window_size[1]+((0.05*window_size[0])+20)))



running = True
while running:
	time_delta = clock.tick(60)/1000.0
	gui_manager()

	# Display Here

	text()

	# draw_maze(window, wall_color=(100,100,100), prints=False)
	manager.update(time_delta)
	manager.draw_ui(window)
	pygame.display.flip()
pygame.quit()