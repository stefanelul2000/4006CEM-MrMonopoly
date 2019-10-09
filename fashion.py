"""import tensorflow as tf
import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt
import os
import tensorboard
import datetime


fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']



train_images = train_images/255.0
train_labels = train_labels/255.0


model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=10)

test_loss,test_acc= model.evaluate(test_images,test_label, verbose = 0)

print("tested Acc:", test_acc)

"""


import tensorflow as tf
from tensorflow import keras
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os
import tensorboard

data = keras.datasets.fashion_mnist

#ML dtataset 

(train_images, train_labels), (test_images, test_label)= data.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images = train_images/255.0
test_images = test_images/255


#plt.imshow(train_images[7], cmap=plt.cm.binary)
#plt.show()
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(512, activation="relu"),
    keras.layers.Dense(128,activation="relu"),
    keras.layers.Dense(128,activation="relu"),
    keras.layers.Dense(10, activation="softmax")
    ])  

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",metrics=["accuracy"])
#logs_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log_dir = os.path.join(
    "logs",
    "fit",
    datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
)
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, update_freq = "epoch", profile_batch=0)

model.fit(train_images,train_labels, epochs=13, callbacks=[tensorboard_callback], validation_data=(test_images,test_label))

test_loss,test_acc= model.evaluate(test_images,test_label, verbose = 0)

sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

print("tested Acc:", test_acc)

#tensorboard --logdir logs/fit