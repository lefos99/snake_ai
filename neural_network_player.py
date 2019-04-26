from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.models import model_from_json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# load data
gameplay_data = pd.read_csv("./snake_data.csv")
Y = gameplay_data['NewDir']
X = gameplay_data.drop(['NewDir',
						'OldDir',
						'snakeStartX','snakeStartY',
						# ~ 'snakeMidX','snakeMidY',
						'snakeEndX','snakeEndY','SnakeLength'], axis=1)
X = np.array(X.values)
n_features = X.shape[1]
print("Using number of features: " + str(X.shape[1]))

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to one hot encoded variables
Y = np_utils.to_categorical(encoded_Y)

# create model
model = Sequential()
model.add(Dense(20, input_shape=(n_features,), activation='relu'))
model.add(Dense(15, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(4, activation='softmax')) 

# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the model
history = model.fit(X, Y, epochs=150, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('model/model_accuracy.png')

# serialize model to JSON
model_json = model.to_json()
with open("model/snake_player_model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model/model.h5")
print("Saved model to disk")
