import csv
import random
import math

class AplliedML:
	def __init__(self, className, normalizedFeature):
		self.feature = []
		self.Dict = []
		self.className = className
		self.normalizedFeature = normalizedFeature
	# shuffule whole dataset
	def shuffleData(self, inputFilename, outputFilename, replaceString):
		with open (inputFilename, 'rU') as readFile:
			reader = csv.DictReader(readFile)
			for line in reader:
				'''
				this part is for convert some nominal data to numeric data, for the new feature
				'''
				if  line['newFeature'] == '#DIV/0!':
					line['newFeature'] = 2
				else:
					line['newFeature']  = float(line['newFeature'])
				
				self.Dict.append(line)

		#self.convertBinary(replaceString)
		#self.normalize()
		random.shuffle(self.Dict)

		with open(outputFilename, 'w+') as resultFile:
			self.feature = ['RegularSeason', 'Season', 'Date', 'HomeTeam', 'HomeTeamScore', 'AwayTeam', 'AwayTeamScore', 'newFeature', 'HomeTeamWin', 'AwayTeamWin', 'NeutralTeamWin']
			writer = csv.writer(resultFile)
			writer.writerow(self.feature)
			dict_writer = csv.DictWriter(resultFile, fieldnames = self.feature)
			dict_writer.writerows(self.Dict)
		
	# class vaule is not nominal 
	def convertBinary(self, replaceString):
	#	replaceString = ['lose', 'win']
		for line in self.Dict:
			for feature in self.className:
				line[feature] = replaceString[int(line[feature])]
	#create folds
	def generateNewfile(self, fileType, filenameId, foldDict):
		filename = fileType + str(filenameId) + ".csv"
		with open(filename, 'w+') as cvFile:
			writer = csv.writer(cvFile)
			writer.writerow(self.feature)
			dict_writer = csv.DictWriter(cvFile, fieldnames = self.feature)
			dict_writer.writerows(foldDict)
	# spilit data into folds 
	def split(self, folds):
		chunks = len(self.Dict) / folds 
		foldDict = []
		for index in range(len(self.Dict)):
			if index % chunks == 0 and len(foldDict) > 0:
				self.generateNewfile('cvFold', index / chunks, foldDict)
				foldDict = []
			foldDict.append(self.Dict[index])
		#self.generateNewfile(len(self.Dict)/ chunks, foldDict)
	def normalize(self):
		normDict = {} # max in first dimension, and min in second dimension
		for line in self.Dict:
			for feature in self.normalizedFeature:
				if  normDict.has_key(feature):  
					maxnum = normDict[feature][0]
					minnum = normDict[feature][1]
				 	maxnum = max(maxnum, int(line[feature]))
				 	minnum = min(minnum, int(line[feature]))
				 	normDict[feature] = [maxnum, minnum]
				else:
					normDict[feature] = [int(line[feature]), int(line[feature])]
		for line in self.Dict:
			for feature in self.normalizedFeature:
				line[feature] = str((float(line[feature]) - normDict[feature][1]) / (normDict[feature][0] - normDict[feature][1]))
	def newFeature(featurePool):
		self.feature.append('ScoreRatio')
		for line in self.Dict:
				self.Dict['ScoreRatio'] = self.Dict['HomeTeamScore'] / self.Dict['AwayTeamScore']


#chunker = AplliedML(['HomeTeamWin', 'AwayTeamWin', 'NeutralTeamWin'], ['Season', 'Date', 'HomeTeamScore', 'AwayTeamScore'])
#chunker.shuffleData('preprocessResult.csv', 'preprocessData.csv', ['lose', 'win'])
#chunker.split(5)
a = [1,2,3]
if not 0 in a:
	print "success"
print a[0]
