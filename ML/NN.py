#!/usr/bin/env python
from __future__ import print_function

"""

The following code has been developed for prototyping purposes of Luftwage Machine Learning Algorithm.
It is heavily based on the example provided by Lasagne for MNIST dataset

Usage

    import NN as nn 
    get_pm5_prediction = nn.setup()
    print(get_pm5_prediction(TMP = 12,WDIR = 334,WSPD = 5.4))

""" 





import sys
import os
import time
import data as data
import numpy as np
import theano
import theano.tensor as T

import lasagne

epocs = 30
N_hidden = 800
N_hidden_2 = 500
N_hidden_3 = 100
learning_rate = 0.00015
# ##################### Function to load the dataset #######################
def load_dataset():
    #Should be written after getting the dataset
    X_train = data.npmatrixListTrain
    y_train = data.npyListTrain
    X_test = data.npmatrixListTest
    y_test = data.npyListTest

    return X_train, y_train, X_test, y_test, X_test, y_test

# ##################### Build the neural network model #######################
# This script supports three types of models. For each one, we define a
# function that takes a Theano variable representing the input and returns
# the output layer of a neural network model built in Lasagne.

def build_mlp(input_var=None):
    # This creates an MLP of two hidden layers , followed by

    # Input layer, specifying the expected input shape of the network
    l_in = lasagne.layers.InputLayer(shape=(None, 3), #number of factors
                                     input_var=input_var)

    # Add a fully-connected, using the linear rectifier, and
    # initializing weights with Glorot's scheme (which is the default anyway):
    l_hid1 = lasagne.layers.DenseLayer(
            l_in, num_units=N_hidden,
            nonlinearity=lasagne.nonlinearities.rectify)

    l_hid1_drop_out = lasagne.layers.DropoutLayer(l_hid1, p=0.5)

    # Another layer:
    l_hid2 = lasagne.layers.DenseLayer(
            l_hid1_drop_out, num_units=N_hidden_2)

    l_hid2_drop_out = lasagne.layers.DropoutLayer(l_hid1, p=0.5)
    # Another layer:
    l_hid3 = lasagne.layers.DenseLayer(
            l_hid2_drop_out, num_units=N_hidden_3)
    
    l_hid3_drop_out = lasagne.layers.DropoutLayer(l_hid1, p=0.5)
    # Finally, we'll add the fully-connected output layer
    l_out = lasagne.layers.DenseLayer(
            l_hid3_drop_out, num_units=1)

    # Each layer is linked to its incoming layer(s), so we only need to pass
    # the output layer to give access to a network in Lasagne:
    return l_out


# ############################# Batch iterator ###############################
# This is just a simple helper function iterating over training data in
# mini-batches of a particular size, optionally in random order. It assumes
# data is available as numpy arrays. For big datasets, you could load numpy
# arrays as memory-mapped files (np.load(..., mmap_mode='r')), or write your
# own custom data iteration function. For small datasets, you can also copy
# them to GPU at once for slightly improved performance. This would involve
# several changes in the main program, though, and is not demonstrated here.

def iterate_minibatches(inputs, targets, batchsize, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]


# ############################## Main program ################################
# Everything else will be handled in our main program now. We could pull out
# more functions to better separate the code, but it wouldn't make it any
# easier to read.


def main(model='mlp', num_epochs=epocs):
    # Load the dataset
    #print("Loading data...")
    X_train, y_train, X_val, y_val, X_test, y_test = load_dataset()

    # Prepare Theano variables for inputs and targets
    input_var = T.dmatrix('inputs')
    target_var = T.dvector('targets')

    # Create neural network model (depending on first command line parameter)
    #print("Building model and compiling functions...")

    network = build_mlp(input_var)

    # Create a loss expression for training, i.e., a scalar objective we want
    # to minimize (for our multi-class problem, it is the cross-entropy loss):
    prediction = lasagne.layers.get_output(network)
    loss = lasagne.objectives.squared_error(prediction, target_var)
    loss = loss.mean()
    # We could add some weight decay as well here, see lasagne.regularization.

    # Create update expressions for training, i.e., how to modify the
    # parameters at each training step. Here, we'll use Stochastic Gradient
    # Descent (SGD) with Nesterov momentum, but Lasagne offers plenty more.
    params = lasagne.layers.get_all_params(network, trainable=True)
    updates = lasagne.updates.sgd(
            loss, params, learning_rate=learning_rate)

    # Create a loss expression for validation/testing. The crucial difference
    # here is that we do a deterministic forward pass through the network,
    # disabling dropout layers.
    test_prediction = lasagne.layers.get_output(network, deterministic = True)
    test_loss = lasagne.objectives.squared_error(test_prediction, 
                                                            target_var)
    test_loss = test_loss.mean()
    # As a bonus, also create an expression for the classification accuracy:
    test_acc = T.mean((test_prediction - target_var)**2)

    # Compile a function performing a training step on a mini-batch (by giving
    # the updates dictionary) and returning the corresponding training loss:
    train_fn = theano.function([input_var, target_var], loss, updates=updates)

    # Compile a second function computing the validation loss and accuracy:
    val_fn = theano.function([input_var, target_var], [test_loss, test_acc])
    
    get_prediction = theano.function([input_var], prediction)

    # Finally, launch the training loop.
    #print("Starting training...")
    # We iterate over epochs:
    for epoch in range(num_epochs):
        # In each epoch, we do a full pass over the training data:
        train_err = 0
        train_batches = 0
        start_time = time.time()
        for batch in iterate_minibatches(X_train, y_train, epocs, shuffle=True):

            inputs, targets = batch
            train_err += train_fn(inputs, targets[1])

            train_batches += 1

        # And a full pass over the validation data:
        val_err = 0
        val_acc = 0
        val_batches = 0
        for batch in iterate_minibatches(X_val, y_val, 28, shuffle=False):
            inputs, targets = batch
            err, acc = val_fn(inputs, targets[1])
            val_err += err
            val_acc += acc
            val_batches += 1

        # Then we print the results for this epoch:
        '''
        print("Epoch {} of {} took {:.3f}s".format(
            epoch + 1, num_epochs, time.time() - start_time))
        print(train_batches)
        print("  training loss:\t\t{:.6f}".format(train_err / train_batches))
        print("  validation loss:\t\t{:.6f}".format(val_err / val_batches))
        print("  validation accuracy:\t\t{:.2f} %".format(val_acc / val_batches * 100))
        '''
    # After training, we compute and print the test error:
    test_err = 0
    test_acc = 0
    test_batches = 0
    for batch in iterate_minibatches(X_test, y_test, 28, shuffle=False):
        inputs, targets = batch
        err, acc = val_fn(inputs, targets[1])
        test_err += err
        test_acc += acc
        test_batches += 1
        '''
    print("Final results:")
    print("  test loss:\t\t\t{:.6f}".format(test_err / test_batches))
    print("  test accuracy:\t\t{:.2f} %".format(test_acc / test_batches * 100))
    '''
    # Optionally, you could now dump the network weights to a file like this:
    np.savez('model.npz', lasagne.layers.get_all_param_values(network))
    
    def get_pred(TMP, WDIR, WSPD):
        return data.denormalize(get_prediction([data.normalize_in([TMP, WDIR, WSPD])]))[0][0]
    return get_pred


def setup():
    get_prediction = main() 
    return get_prediction 
