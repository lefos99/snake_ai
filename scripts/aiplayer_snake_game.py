#	SNAKE GAME
#	Author : Apaar Gupta (@apaar97)
#	Python 3.5.2 Pygame

import pygame
import sys
import time
import random
import csv
import numpy as np

from keras.models import model_from_json
import pandas as pd
import yaml

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
foodPos = [400, 50]
foodSpawn = True
direction = 'RIGHT'
changeto = ''
score = 0


# Game Over
def gameOver():
	myFont = pygame.font.SysFont('monaco', 72)
	GOsurf = myFont.render("Game Over", True, red)
	GOrect = GOsurf.get_rect()
	GOrect.midtop = (320, 25)
	playSurface.blit(GOsurf, GOrect)
	showScore(0)
	print("Score: " + str(score) + "!")
	pygame.display.flip()
	time.sleep(4)
	pygame.quit()
	sys.exit()

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
		

with open("../conf/conf.yaml", 'r') as stream:
	try:
		param = yaml.load(stream)
	except yaml.YAMLError as exc:
		print(exc)

wait = input("PRESS ENTER TO CONTINUE.")

# load json and create model
with open('../model/snake_player_model.json', 'r') as json_file:
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("../model/model.h5")
	print("Loaded ai player from disk!")

	while True:
		
		cur_data_list = np.array([createFeatureArray(param, foodPos, snakePos, snakeBody, direction, width, height)])
		current_pred = loaded_model.predict(x=cur_data_list)
		next_dir = np.argmax(current_pred)
		
		# Translate the output of the nn to direction
		if next_dir == 2:
			changeto = 'RIGHT'
		if next_dir == 1:
			changeto = 'LEFT'
		if next_dir == 0:
			changeto = 'UP'
		if next_dir == 3:
			changeto = 'DOWN'
		print("Change direction to " + changeto)	
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
	
		# Validate direction
		if changeto == 'RIGHT' and direction != 'LEFT':
			direction = changeto
		elif changeto == 'LEFT' and direction != 'RIGHT':
			direction = changeto
		elif changeto == 'UP' and direction != 'DOWN':
			direction = changeto
		elif changeto == 'DOWN' and direction != 'UP':
			direction = changeto
			
		# Help Snake trun 180 degrees
		if param["rotation_help"] == True:
			if changeto == 'RIGHT' and direction == 'LEFT':
				direction = 'UP'
				print("Help was needed!")
			elif changeto == 'LEFT' and direction == 'RIGHT':
				direction = 'UP'
				print("Help was needed!")
			elif changeto == 'UP' and direction == 'DOWN':
				direction = 'RIGHT'
				print("Help was needed!")
			elif changeto == 'DOWN' and direction == 'UP':
				direction = 'RIGHT'
				print("Help was needed!")

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
		fpsController.tick(20)
