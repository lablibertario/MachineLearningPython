# Import the necessary packages
import numpy as np
import random
from ml_lib import *
import copy
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
import warnings
warnings.filterwarnings("ignore")


# Returns predictions with the input test data, class labels, hidden layer parameters, output layer parameters and hidden unit count
def getEstimate(attributes,olParam,hlParam,otcmVal,huCount,testingEstimate):
    for i in range(attributes.shape[0]):
        prevEst, otcmMax = 0, 0
        currEst = []
        hlOutput = [logisticFunction(hlParam[j],attributes[i]) for j in range(huCount)]

        for y in range(len(otcmVal)):
            currEst.append(softmaxFunction(olParam,hlOutput,y,otcmVal))
            if(currEst[y] > prevEst):
                otcmMax = y
                prevEst = currEst[y]
        testingEstimate.append(otcmVal[otcmMax])
    return testingEstimate   
    
    
# To get the final parameters by using iterative parameter update
def gradient_descent(attributes, outcomes, otcmVal, huCount, iterCountMax, learningRate, threshold, olLearningRate, beta):
    otcmValCount = len(otcmVal)
    attRowCount, attColCount = attributes.shape
        
    hlOutput = np.empty([attRowCount,huCount])
    currEst = np.empty([attRowCount,otcmValCount])    
    olParam = np.random.rand(otcmValCount,huCount)/10
    hlParam = np.random.rand(huCount,attColCount)/10
    hlOutput = np.transpose(logisticFunction(np.transpose(hlParam),np.transpose(attributes)))
    
    for itr in range(attRowCount):
        for intitr in range(otcmValCount):
            currEst[itr,intitr] = softmaxFunction(olParam,hlOutput[itr],intitr,otcmVal)
            
    for mainitr in range(iterCountMax):
        hlOutput = np.transpose(logisticFunction(np.transpose(hlParam),np.transpose(attributes)))
        for itr in range(attRowCount):
            for intitr in range(otcmValCount):
                currEst[itr,intitr] = softmaxFunction(olParam,hlOutput[itr],intitr,otcmVal)

        for intitr in range(otcmValCount):
            paramCorrection = []
            for itr in range(attRowCount):
                paramCorrection.append((currEst[itr,intitr] - (1 if outcomes[itr]==intitr else 0)) * hlOutput[itr])
            
            # Update output layer params with correction using momentum
            if intitr >= 2:
                olParam[intitr] -= learningRate * sum(paramCorrection) - beta*(olParam[intitr-1]-olParam[intitr-2])
            else:
				olParam[intitr] -= learningRate * sum(paramCorrection)
			
        for intitr in range(huCount):
            paramCorrection = []
            for itr in range(attRowCount):
                paramCorrection1 = []
                for yval in range(otcmValCount):
                    paramCorrection1.append((currEst[itr,yval] - (1 if outcomes[itr]==yval else 0)) * olParam[yval,intitr])
                paramCorrection.append(sum(paramCorrection1) * hlOutput[itr,intitr] * (1-hlOutput[itr,intitr]) * attributes[itr])
            
            # Update hidden layer params with correction using momentum
            if intitr >= 2:
                hlParam[intitr] -= learningRate * sum(paramCorrection) - beta*(hlParam[intitr-1]-hlParam[intitr-2])
            else:
				hlParam[intitr] -= learningRate * sum(paramCorrection)
			
    return olParam,hlParam
