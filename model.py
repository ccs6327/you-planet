#!/usr/bin/env python
import os
import sys
import csv
import numpy as np
import warnings
from sklearn import preprocessing
from sklearn.ensemble import AdaBoostClassifier
from numpy import inf
from sklearn.externals import joblib

FILE_X_TRAIN = "data/trainX.txt"
FILE_X_DEV = "data/devX.txt"
FILE_Y_TRAIN = "data/trainY_sev.txt"
FILE_Y_DEV = "data/devY_sev.txt"
FILE_Y_TRAIN_BIN = "data/trainY_bin.txt"
FILE_Y_DEV_BIN = "data/devY_bin.txt"
FILE_Y_TRAIN_MULTI = "data/trainY_multi.txt"
FILE_Y_DEV_MULTI = "data/devY_multi.txt"
MODEL_NAME = "model.pkl"

MULTI = ["minimal", "mild", "moderate", "moderately_severe", "severe"]

def getX(fileName):
    X = []
    with open(fileName, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        X = np.array([ [ float(eaVal) for eaVal in row] for row in reader])
        # safety to check every row
        n_feats = len(X[0])
        i = 0
        for x in X:
            i += 1
            if n_feats != len(x):
                print('Warning, some x has different number of features!!')
                print(fileName+":"+str(i)+" has "+ str(len(x)) + " features != " + str(n_feats))
                sys.exit(1)
            if np.any(np.isnan(x)):
                print("Warning:"+fileName+":"+str(i)+" has NaN values")
                sys.exit(1)
            if not np.all(np.isfinite(x)):
                print("Warning:"+fileName+":"+str(i)+" has Inf values") 
                x[np.isneginf(x)] = 0;np.finfo(np.float64).min
                x[np.isposinf(x)] = 0; np.finfo(np.float64).max
                X[i-1] = x
                #print x
                #sys.exit(1)
    return X, n_feats, len(X)

def getY(filename):
    y = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        y = [ int(row[0]) for row in reader ]
    return y, len(y)

def read_train_dev_files(trainx, devx, trainy, devy):
    warnings.filterwarnings("ignore")

    X_train, n_feats_train, k_x_train = getX(trainx)
    X_dev, n_feats_dev, k_x_dev = getX(devx)
    y_train, k_y_train = getY(trainy)
    y_dev, k_y_dev = getY(devy)

    # some sanity checks on n_feats
    if n_feats_train != n_feats_dev:
        print('Error n_feats in train and dev. They are not equal.')
        sys.exit(1)
    n_feats = n_feats_train

    # sanity checks for k_train
    if k_x_train != k_y_train:
        print('Error, train is of different size')
        sys.exit(1)
    k_train = k_x_train
    if k_x_dev != k_y_dev:
        print('Error, dev is of different size')
        sys.exit(1)
    k_dev = k_x_dev

    print("Data has " + str(n_feats) + " features and " + str(k_train) + " training points and " + str(k_dev) + " dev points." )
    return np.array(X_train), np.array(y_train), np.array(X_dev), np.array(y_dev)

def trainMultiClass():
    x_train_file_name = FILE_X_TRAIN
    x_dev_file_name = FILE_X_DEV
    y_train_file_name = FILE_Y_TRAIN_MULTI
    y_dev_file_name = FILE_Y_DEV_MULTI
    X_train, y_train, X_dev, y_dev = read_train_dev_files(x_train_file_name, x_dev_file_name, y_train_file_name, y_dev_file_name)
    cls = AdaBoostClassifier(random_state=13370)
    cls.fit(X_train, y_train)
    joblib.dump(cls, MODEL_NAME) 

def averageFeatureInFile(csvFilename):
	if csvFilename.endswith(".csv"):
		with open(csvFilename, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			tempFeatureRows = []
			for row in spamreader:
				tempFeatureRow = []
				for cell in row:
					tempFeatureCellValue = float(cell)
					tempFeatureRow.append(tempFeatureCellValue)
				tempFeatureRow = np.array(tempFeatureRow)
				tempFeatureRows.append(tempFeatureRow)
			tempFeatureRows = np.array(tempFeatureRows)
			averageRow = np.mean(tempFeatureRows, axis=0)
			stdRow = np.std(tempFeatureRows, axis=0)
			featureRow = np.concatenate([averageRow, stdRow])

			return featureRow

def predict(filename):
	X = averageFeatureInFile(filename)
	if not os.path.isfile(MODEL_NAME):
		trainMultiClass()
	cls = joblib.load(MODEL_NAME) 
	
	Y = cls.predict([X])
	return MULTI[Y[0]]

def main():
	if len(sys.argv) < 2:
		print "please insert the feature filename"
		return

	filename = sys.argv[1]
	print predict(filename)
	
	
if __name__ == "__main__": 
	main()