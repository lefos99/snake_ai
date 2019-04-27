#	SNAKE GAME
#	Author : Apaar Gupta (@apaar97)
#	Python 3.5.2 Pygame

import pygame
import sys
import time
import random
import csv
import pandas as pd
from helper import *

# Pygame Init
init_status = pygame.init()
if init_status[1] > 0:
	print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
	sys.exit()
else:
	print("(+) Pygame initialised successfully ")

# Play Surface
size = width, height = 640, 320
playSurface = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")

# Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)

# FPS controller
fpsController = pygame.time.Clock()

# Game settings
delta = 10
snakePos = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]
foodPos = [random.randrange(1, width // 10) * delta, random.randrange(1, height // 10) * delta]
foodSpawn = True
direction = 'RIGHT'
changeto = 'RIGHT'
score = 0


# Game Over
def gameOver():
	myFont = pygame.font.SysFont('monaco', 72)
	GOsurf = myFont.render("Game Over", True, red)
	GOrect = GOsurf.get_rect()
	GOrect.midtop = (320, 25)
	playSurface.blit(GOsurf, GOrect)
	showScore(0)
	pygame.display.flip()
	time.sleep(4)
	pygame.quit()
	sys.exit()

# ~ def translateDirToInt(direction):
	# ~ dirinteger = 0
	# ~ if direction == 'UP':
		# ~ dirinteger = 0
	# ~ elif direction == 'LEFT':
		# ~ dirinteger = 1
	# ~ elif direction == 'RIGHT':
		# ~ dirinteger = 2
	# ~ elif direction == 'DOWN':
		# ~ dirinteger = 3
	# ~ return dirinteger
		
# Show Score
def showScore(choice=1):
	SFont = pygame.font.SysFont('monaco', 32)
	Ssurf = SFont.render("Score  :  {0}".format(score), True, black)
	Srect = Ssurf.get_rect()
	if choice == 1:
		Srect.midtop = (80, 10)
	else:
		Srect.midtop = (320, 100)
	playSurface.blit(Ssurf, Srect)

# Save the training data in a csv file
def trainingDataToString(filewriter, foodPos, snakePos, snakeBody, old_direction, new_direction):
	
	data_list = [foodPos[0], foodPos[1], snakePos[0], snakePos[1], 
				snakeBody[0][0], snakeBody[0][1], 
				snakeBody[int(len(snakeBody)/2)+1][0],
				snakeBody[int(len(snakeBody)/2)+1][1], 
				snakeBody[-1][0], snakeBody[-1][1],
				len(snakeBody), translateDirToInt(old_direction),
				translateDirToInt(new_direction)]
	data_string = [str(i) for i in data_list]
	filewriter.writerow(data_string)

df = pd.read_csv('snake_data.csv')
if(df.empty):
	mode = 'w'
	print("No one has played yet...")
else:
	mode = 'a'
	print("Someone has already played...")

with open('snake_data.csv', mode) as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',')
	data_header = ["foodX", "foodY", "snakeX", "snakeY", "snakeStartX", 
				"snakeStartY", "snakeMidX", "snakeMidY", "snakeEndX", 
				"snakeEndY", "SnakeLength", "OldDir", "NewDir"]
	if mode == 'w':
		filewriter.writerow(data_header)
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					changeto = 'RIGHT'
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					changeto = 'LEFT'
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					changeto = 'UP'
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					changeto = 'DOWN'
				if event.key == pygame.K_ESCAPE:
					pygame.event.post(pygame.event.Event(pygame.QUIT))
					
		# Save data for each instance of the game
		trainingDataToString(filewriter, foodPos, snakePos, snakeBody, direction, changeto)
		
		# Validate direction
		if changeto == 'RIGHT' and direction != 'LEFT':
			direction = changeto
		elif changeto == 'LEFT' and direction != 'RIGHT':
			direction = changeto
		elif changeto == 'UP' and direction != 'DOWN':
			direction = changeto
		elif changeto == 'DOWN' and direction != 'UP':
			direction = changeto

		# Update snake position
		if direction == 'RIGHT':
			snakePos[0] += delta
		if direction == 'LEFT':
			snakePos[0] -= delta
		if direction == 'DOWN':
			snakePos[1] += delta
		if direction == 'UP':
			snakePos[1] -= delta
		# Snake body mechanism
		snakeBody.insert(0, list(snakePos))
		if snakePos == foodPos:
			foodSpawn = False
			score += 1
		else:
			snakeBody.pop()
		if foodSpawn == False:
			foodPos = [random.randrange(1, width // 10) * delta, random.randrange(1, height // 10) * delta]
			foodSpawn = True

		playSurface.fill(white)
		for pos in snakeBody:
			pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], delta, delta))
		pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], delta, delta))

		# Bounds
		if snakePos[0] >= width or snakePos[0] < 0:
			gameOver()
		if snakePos[1] >= height or snakePos[1] < 0:
			gameOver()

		# Self hit
		for block in snakeBody[1:]:
			if snakePos == block:
				gameOver()
		
		showScore()
		pygame.display.flip()
		fpsController.tick(10)
