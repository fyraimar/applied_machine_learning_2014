import csv
class tunedFold:
	def __init__(self):
		self.table = []
		self.feature = ['RegularSeason', 'Season', 'Date', 'HomeTeam', 'AwayTeam', 'HistoryHomeWin', 'HistoryHomeLose', 'newFeature', 'HomeTeamWin']
		self.cv = []

	def split(self, folds, inputFilename):
		with open (inputFilename, 'rU') as readFile:
			reader = csv.DictReader(readFile)
			for line in reader:
				self.table.append(line)

		chunks = len(self.table) / folds 
		fold = []
		for index in range(len(self.table)):
			if index % chunks == 0 and len(fold) > 0:
				#self.generateNewfile('newCVFold', index / chunks, fold)
				self.cv.append(fold)
				fold = []
			fold.append(self.table[index])
		self.cv.append(fold)
		#self.generateNewfile('newCVFold', folds, fold)
		innerCV = []
		#heldSet = [] 
		foldNum = 0
		for heldFold in self.cv:
			for trainFold in self.cv:
				if trainFold != heldFold:
					innerCV.extend(trainFold)
			foldNum = foldNum + 1
			self.generateNewfile('newCVFold', foldNum, innerCV)
			self.generateNewfile('newCVTestFold', foldNum, heldFold)	 

	def generateNewfile(self, fileName, fileNameId, foldDict):
		filename = fileName + str(fileNameId) + ".csv"
		with open(filename, 'w+') as cvFile:
			writer = csv.writer(cvFile)
			writer.writerow(self.feature)
			dict_writer = csv.DictWriter(cvFile, fieldnames = self.feature)
			dict_writer.writerows(foldDict)

chunker = tunedFold()
chunker.split(5, 'newCV.csv')
