#tetrisAI.py
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from copy import deepcopy
import Tetris
#generate model
            

def generateRandomModel():
    customLossFunction = 'mse' #<------------------------------------------needs to be changed!!!
    
    tempInitializer = tf.keras.initializers.RandomNormal(mean=0., stddev=1)
    biasInitializer = keras.initializers.Zeros()
    tempModel = keras.Sequential([
    keras.layers.Input(shape=(20, 10)),
    keras.layers.Dense(200,kernel_initializer=tempInitializer,bias_initializer = biasInitializer),
    keras.layers.Dense(200,kernel_initializer=tempInitializer,bias_initializer = biasInitializer),
    keras.layers.Dense(200,kernel_initializer=tempInitializer,bias_initializer = biasInitializer),
    keras.layers.Dense(1, name='endStateQuality')
    ])
    tempModel.compile(optimizer = 'adam',
    loss = customLossFunction,  
    metrics = ['accuracy'],
    )   
    tempModel.build((None,1))
    return tempModel

epochs = 10
model = generateRandomModel()

game = Tetris.AITetrisGame()
game.playTetris(model) 

"""
for epoch in range(epochs):

   
    result = model.fit(inputVectors,outputVectors,
        epochs = 1, # number of iteration
    )
    
        resultsArray.append(result)
        lossesArray.append(resultsArray[i].history['loss'][0])
    minLossIndex = np.argmax(lossesArray)
    fig = plt.figure(figsize=(6, 6))
    grid = plt.GridSpec(2, 2, hspace=0.2, wspace=0.2)
    main_ax = fig.add_subplot(grid[0,0:])
    lossAx = fig.add_subplot(grid[1,0])
    neuralNetAx = fig.add_subplot(grid[-1, 1:])
    neuralNetAx.axis('off')
    printModel(modelArray[minLossIndex],inputVectors,outputVectors,main_ax)
    visualizeNeuralNet.drawKerasNeuralNet(neuralNetAx,modelArray[minLossIndex])
    losses.append(resultsArray[minLossIndex].history['loss'][0])
    accuracies.append(resultsArray[minLossIndex].history['accuracy'][0])
    lossAx.plot(losses,color = 'orange')
    accurAx=lossAx.twinx()
    accurAx.plot(accuracies,color = 'green')
    lossAx.set_yscale('log')
    plt.savefig("spiralGifFits/spiralFit{}.png".format(epoch))
    filenames.append("spiralGifFits/spiralFit{}.png".format(epoch))
    
    
    modelArray[np.argmax(lossesArray)] = mutateModel(crossOverNets(modelArray[np.argsort(lossesArray)[-2]],modelArray[minLossIndex]))

    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave('modelFitting.gif', images)
"""