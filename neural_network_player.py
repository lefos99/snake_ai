from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from keras.utils.vis_utils import plot_model
from sklearn.preprocessing import LabelEncoder
from keras.models import model_from_json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml

with open("conf.yaml", 'r') as stream:
	try:
		param = yaml.load(stream)
	except yaml.YAMLError as exc:
		print(exc)

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# load the features you want to use in the nn
drop_list = []
for key in param["game_features"]:
	if param["game_features"][key] == False:
		drop_list.append(str(key))

# load data
gameplay_data = pd.read_csv("./snake_data.csv")
Y = gameplay_data['NewDir']
X = gameplay_data.drop(drop_list, axis=1)
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
model.add(Dense(param["nn"][str(1)+"_layer"], input_shape=(n_features,), activation='relu'))
for i in range(param["nn"]["n_layers"]):
	model.add(Dense(param["nn"][str(i+1)+"_layer"], activation='relu'))
model.add(Dense(param["nn"][str(i+1)+"_layer"], activation='softmax')) 

# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the model
history = model.fit(X, Y, epochs=param["nn"]["epochs"], batch_size=param["nn"]["batch_size"])

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# serialize model to JSON
model_json = model.to_json()
with open("model/snake_player_model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model/model.h5")
print("Saved model to disk")

# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig('model/model_accuracy.png')
plot_model(model, to_file='model/model_plot.png', show_shapes=True, show_layer_names=True)
