from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.models import model_from_json
import numpy as np
import pandas as pd

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# load data
gameplay_data = pd.read_csv("./snake_data.csv")
X = gameplay_data.drop(['NewDir'], axis=1)
print(X)
X = np.array(X.values)
# ~ X = X[:,0:10]
Y = gameplay_data['NewDir']
print(X)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to one hot encoded variables
Y = np_utils.to_categorical(encoded_Y)

# create model
model = Sequential()
model.add(Dense(30, input_shape=(12,), activation='relu'))
model.add(Dense(15, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(4, activation='softmax')) 

# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the model
model.fit(X, Y, epochs=300, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = model.to_json()
with open("snake_player_model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
