
def translateDirToInt(direction):
	dirinteger = 0
	if direction == 'UP':
		dirinteger = 0
	elif direction == 'LEFT':
		dirinteger = 1
	elif direction == 'RIGHT':
		dirinteger = 2
	elif direction == 'DOWN':
		dirinteger = 3
	return dirinteger

# Returns the distance in direction x and y between body and head of snake.
def distanceToBody(snakePos, snakeBody, width, height):
	# define max possible distances
	distOwnBody1, distOwnBody2, distOwnBody3, distOwnBody4 = snakePos[1], width - snakePos[0], height - snakePos[1], snakePos[0]	
	for bodyPart in snakeBody:
		if snakePos[0] == bodyPart[0] and snakePos[1] > bodyPart[1]:
			distOwnBody1 = min(snakePos[1] - bodyPart[1], distOwnBody1)
		if snakePos[0] == bodyPart[0] and snakePos[1] < bodyPart[1]:
			distOwnBody3 = min(bodyPart[1] - snakePos[1], distOwnBody3) 
		if snakePos[1] == bodyPart[1] and snakePos[0] < bodyPart[0]:
			distOwnBody2 = min(bodyPart[0] - snakePos[0], distOwnBody4)
		if snakePos[1] == bodyPart[1] and snakePos[0] > bodyPart[0]:
			distOwnBody4 = min(snakePos[0] - bodyPart[0], distOwnBody2)
	
	return distOwnBody1, distOwnBody2, distOwnBody3, distOwnBody4
		
# Save the training data in a csv file
def trainingDataToString(filewriter, foodPos, snakePos, snakeBody, old_direction, new_direction, width, height):
	
	distOwnBody1, distOwnBody2, distOwnBody3, distOwnBody4 = distanceToBody(snakePos, snakeBody, width, height)
	data_list = [snakePos[1], width - snakePos[0], height - snakePos[1], snakePos[0],
				snakePos[1] - foodPos[1], snakePos[0] - foodPos[0], 
				distOwnBody1, distOwnBody2, distOwnBody3, distOwnBody4,
				translateDirToInt(old_direction),
				translateDirToInt(new_direction)]
	data_string = [str(i) for i in data_list]
	filewriter.writerow(data_string)
	
# Create the array of features
def createFeatureArray(param, foodPos, snakePos, snakeBody, direction, width, height):
	feature_array = []
	
	distOwnBody1, distOwnBody2, distOwnBody3, distOwnBody4 = distanceToBody(snakePos, snakeBody, width, height)
	
	if param["game_features"]["distWall1"] == True:
		feature_array.append(snakePos[1])
	if param["game_features"]["distWall2"] == True:
		feature_array.append(width - snakePos[0])
	if param["game_features"]["distWall3"] == True:
		feature_array.append(height - snakePos[1])
	if param["game_features"]["distWall4"] == True:
		feature_array.append(snakePos[0])
	if param["game_features"]["distFood1"] == True:
		feature_array.append(snakePos[1] - foodPos[1])
	if param["game_features"]["distFood2"] == True:
		feature_array.append(snakePos[0] - foodPos[0])
	if param["game_features"]["distOwnBody1"] == True:
		feature_array.append(distOwnBody1)
	if param["game_features"]["distOwnBody2"] == True:
		feature_array.append(distOwnBody2)
	if param["game_features"]["distOwnBody3"] == True:
		feature_array.append(distOwnBody3)
	if param["game_features"]["distOwnBody4"] == True:
		feature_array.append(distOwnBody4)
	if param["game_features"]["OldDir"] == True:
		feature_array.append(translateDirToInt(direction))
	
	return feature_array
