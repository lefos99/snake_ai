
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
	
# Create the array of features
def createFeatureArray(param, foodPos, snakePos, snakeBody, direction):
	feature_array = []
	if param["game_features"]["foodX"] == True:
		feature_array.append(foodPos[0])
	if param["game_features"]["foodY"] == True:
		feature_array.append(foodPos[1])
	if param["game_features"]["snakeX"] == True:
		feature_array.append(snakePos[0])
	if param["game_features"]["snakeY"] == True:
		feature_array.append(snakePos[1])
	if param["game_features"]["snakeStartX"] == True:
		feature_array.append(snakeBody[0][0])
	if param["game_features"]["snakeStartY"] == True:
		feature_array.append(snakeBody[0][1])
	if param["game_features"]["snakeMidX"] == True:
		feature_array.append(snakeBody[int(len(snakeBody)/2)+1][0])
	if param["game_features"]["snakeMidY"] == True:
		feature_array.append(snakeBody[int(len(snakeBody)/2)+1][1])
	if param["game_features"]["snakeEndX"] == True:
		feature_array.append(snakeBody[-1][0])
	if param["game_features"]["snakeEndY"] == True:
		feature_array.append(snakeBody[-1][1])
	if param["game_features"]["SnakeLength"] == True:
		feature_array.append(len(snakeBody))
	if param["game_features"]["OldDir"] == True:
		feature_array.append(translateDirToInt(direction))
	
	return feature_array
