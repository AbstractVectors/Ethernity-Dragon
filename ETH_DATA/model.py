import random
import numpy
from tensorflow import keras


ratio = 0.7
window_size = 40
file = open('eth_1_hour_price.csv')
master = []
data = file.read().split()[1:]
n = 0
for i in range(len(data) - window_size - 1):
    l = []
    for _ in range(window_size):
        d = float(data[i + window_size].split(',')[4])
        l.append(d)
    master.append([l, float(data[i + window_size].split(',')[4])])


random.shuffle(master)
training = master[:int(len(master) * ratio)]
testing = master[int(len(master) * ratio):]
train_xs = []
train_ys = []
for x, y in training:
    train_ys.append(x)
    train_ys.append(y)
train_xs = numpy.array(train_xs)
train_ys = numpy.array(train_ys)
val_xs = []
val_ys = []
for x, y in training:
    val_xs.append(x)
    val_ys.append(y)
val_xs = numpy.array(val_xs)
val_ys = numpy.array(val_ys)


model = keras.models.Sequential([
    keras.layers.Conv1D(filters=64, kernel_size=3,
        strides=1,
        activation='relu',
        padding='causal',
        input_shape=[window_size, 1]
    ),
    keras.layers.Bidirectional(keras.layers.LSTM(32), return_sequences=True),
    keras.layers.Bidirectional(keras.layers.LSTM(32)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1)
])

model.summary()
model.compile(optimizer='sgd', loss='huber', metrics=['acc'])
model.fit(data=(train_xs, train_ys), epochs=500, validation_data=(val_xs, val_ys))
