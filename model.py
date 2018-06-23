#!/usr/bin/env python

from sklearn.externals import joblib
import sys
import csv
import numpy as np

MULTI = ["minimal", "mild", "moderate", "moderately_severe", "severe"]

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

def main():
	if len(sys.argv) < 2:
		print "please insert the feature filename"
		return

	filename = sys.argv[1]
	X = averageFeatureInFile(filename)
	
	cls = joblib.load('model.pkl') 
	
	Y = cls.predict([X])
	print MULTI[Y[0]]
	
	
if __name__ == "__main__": 
	main()