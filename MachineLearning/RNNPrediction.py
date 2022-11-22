import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.python.keras.engine.base_preprocessing_layer import PreprocessingLayer
import requests
import urllib.parse
import math
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import cupy as cp
import seaborn
from numba import cuda
import dataset
from importlib import reload
import os.path
import sys

reload(dataset)
print(tf.config.list_physical_devices('GPU'))
tf.compat.v1.enable_eager_execution()

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
# (nothing gets printed in Jupyter, only if you run it standalone)
sess = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(sess)  # set this TensorFlow session as the default session for Keras
keras.backend.set_epsilon(1)


def savedata(xtrain, ytrain, xtest, ytest, name="data"):
    np.savez_compressed(os.path.join("saveddata", name), timetrain=xtrain[0], idxtrain=xtrain[1], typetrain=xtrain[2],
                        totidxtrain=xtrain[3], ytrain=ytrain,
                        timetest=xtest[0], idxtest=xtest[1], typetest=xtest[2], totidxtest=xtest[3], ytest=ytest)


def loaddata(name="data"):
    with np.load(os.path.join("saveddata", (name if name.endswith(".npz") else name + ".npz"))) as data:
        xtrain = [data["timetrain"], data["idxtrain"], data["typetrain"], data["totidxtrain"]]
        ytrain = data["ytrain"]
        xtest = [data["timetest"], data["idxtest"], data["typetest"], data["totidxtest"]]
        ytest = data["ytest"]
    return xtrain, ytrain, xtest, ytest, xtrain[0].shape[1]


if len(sys.argv)>1 and sys.argv[1]=="new":
    lookback = 60
    '''xtrain, ytrain, xtest, ytest = dataset.getdata(lookback=lookback, items=[
        ("★ M9 Bayonet | Fade (Factory New)", "Knife"),
        ("StatTrak™ AK-47 | Ice Coaled (Factory New)", "Gun"),
        ("Recoil Case", "Case"),
        ("CS:GO Weapon Case", "Case"),
        ("Sticker | s1mple (Gold) | Katowice 2019", "Sticker"),
        ("Sealed Graffiti | NaCl (Shark White)", "Graffiti"),
        ("Canals Pin", "Pin"),
        ("StatTrak™ Music Kit | Hundredth, FREE", "Music"),
        ("Stockholm 2021 Challengers Patch Pack", "Patch"),
        ("Number K | The Professionals", "Agent"),
        ("★ Broken Fang Gloves | Needle Point (Field-Tested)", "Gloves"),
        ("AWP | Asiimov (Well-Worn)", "Gun"),
        # ("AWP | Asiimov (Factory New)", "Gun"),
        # ("★ Broken Fang Gloves | Needle Point (Well-Worn)", "Gloves"),
    ])'''
    xtrain, ytrain, xtest, ytest = dataset.getdata(lookback=lookback, items=[
        ("Recoil Case", "Case"),
        ("CS:GO Weapon Case", "Case"),
        ("Dreams & Nightmares Case", "Case"),
        ("Operation Riptide Case", "Case"),
        ("Snakebite Case", "Case"),
        ("Fracture Case", "Case"),
        ("Danger Zone Case", "Case"),
        ("Clutch Case", "Case"),
        ("Prisma 2 Case", "Case"),
        ("Horizon Case", "Case"),
        ("Gamma Case", "Case"),
        ("Operation Bravo Case", "Case")
    ])
    savedata(xtrain, ytrain, xtest, ytest)
else:
    xtrain, ytrain, xtest, ytest, lookback = loaddata()

rnnlayer = layers.GRU

'''
def getmodel():
    """m = keras.Sequential([
        ,
        layers.Dense(80),
        layers.GRU(80, return_sequences=False, input_shape=(lookback, 1)),
        layers.Dense(25),
        layers.Dense(1),
    ])"""

    # vocab = ["Gloves", "Agent", "Patch", "Music", "Pin", "Graffiti", "Sticker", "Case", "Knife", "Gun"]
    vocab = ["Case"]
    timeinput = keras.Input(shape=(lookback, 1))
    idxinput = keras.Input(shape=(1), dtype=tf.float32)
    typeinput = keras.Input(shape=(1), dtype=tf.string)
    totalidxinput = keras.Input(shape=(1), dtype=tf.float32)

    typeinput2 = layers.StringLookup(vocabulary=vocab, output_mode="multi_hot")(typeinput)
    typeinput2 = layers.Reshape((typeinput2.shape[1], 1))(typeinput2)

    idxinput2 = layers.Reshape((idxinput.shape[1], 1))(idxinput)
    totalidxinput2 = layers.Reshape((idxinput.shape[1], 1))(totalidxinput)
    timeinput2 = layers.Normalization()(timeinput)

    x = layers.Concatenate(axis=1)([timeinput2, idxinput2, typeinput2, totalidxinput2])
    x = layers.Reshape((1, x.shape[1]))(x)

    x = layers.Dense(200)(x)
    x = rnnlayer(200, return_sequences=True)(x)
    x = layers.Dense(120)(x)
    x = rnnlayer(120, return_sequences=True)(x)
    x = layers.Dense(80)(x)
    x = rnnlayer(80, return_sequences=True)(x)
    x = layers.Dense(40)(x)
    x = rnnlayer(40, return_sequences=False)(x)
    # x = layers.Dense(25)(x)
    for i in range(5):
        x = layers.Dense(25)(x)
    x = layers.Dense(1, activation="sigmoid")(x)

    m = keras.Model(inputs=[timeinput, idxinput, typeinput, totalidxinput], outputs=x)

    m.build((None, lookback, 1))
    m.summary()
    return m
'''


def getmodel():
    timeinput = keras.Input(shape=(lookback, 1))
    idxinput = keras.Input(shape=(1), dtype=tf.float32)
    typeinput = keras.Input(shape=(1), dtype=tf.string)
    totalidxinput = keras.Input(shape=(1), dtype=tf.float32)

    vocab = ["Case"]

    typeinput2 = layers.StringLookup(vocabulary=vocab, output_mode="multi_hot")(typeinput)
    typeinput2 = layers.Reshape((typeinput2.shape[1], 1))(typeinput2)

    idxinput2 = layers.Reshape((idxinput.shape[1], 1))(idxinput)
    totalidxinput2 = layers.Reshape((idxinput.shape[1], 1))(totalidxinput)
    timeinput2 = layers.Normalization()(timeinput)

    for i in range(5):
        timeinput2 = rnnlayer(80, return_sequences=True)(timeinput2)
    timeinput2 = rnnlayer(80, return_sequences=False)(timeinput2)
    timeinput2 = layers.Reshape((timeinput2.shape[1], 1))(timeinput2)

    x = layers.Concatenate(axis=1)([timeinput2, idxinput2, typeinput2, totalidxinput2])
    x = layers.Reshape((1, x.shape[1]))(x)

    for i in range(20):
        x = layers.Dense(20)(x)

    x = layers.Dense(1, activation="relu")(x)
    m = keras.Model(inputs=[timeinput, idxinput, typeinput, totalidxinput], outputs=x)

    m.build((None, lookback, 1))
    m.summary()
    return m


def trainmodel():
    model = getmodel()

    model.compile(optimizer="adam", loss=keras.metrics.MeanAbsolutePercentageError(),
                  metrics=["accuracy", keras.metrics.RootMeanSquaredError(),
                           keras.metrics.MeanAbsolutePercentageError(),
                           "binary_crossentropy"])
    history = model.fit(xtrain, ytrain, batch_size=32, epochs=20, verbose=1)

    model.save("model.hdf5")

    model.evaluate(xtrain, ytrain)
    model.evaluate(xtest, ytest)
    return model


def loadmodel():
    model = models.load_model("model.hdf5")
    model.summary()
    return model


if __name__ == "__main__":
    trainmodel()
