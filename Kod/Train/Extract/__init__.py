import os, cv2
from skimage.feature import hog
from numpy import *

class HOG:

	def __init__(self, BINS, PIXELS, CELLS):
		self.bins = BINS
		self.pixels = PIXELS
		self.cells = CELLS


	def getDescriptor(self, img):
		fd = hog(img, orientations = self.bins, pixels_per_cell= self.pixels, 
		cells_per_block= self.cells, visualise=False)
	
		return fd

class Extract:

	def __init__(self, hog, cut):
		self.HOG = hog
		self.CUT = cut


	def getSamples(self, pos, neg, *args):
		
		lPos = 100000000
		lNeg = 100000000

		if len(args) == 2:
			lPos = args[0]
			lNeg = args[1]

		listSamples = list()
		listClass = list()

		for pic in pos:
			pos_cuts = self.CUT.getPeople(pic[ 0 ], pic[ 1 ])
			for p in pos_cuts:
				if lPos == 0:
					break
				descriptor = self.HOG.getDescriptor(p)
				listSamples.append(descriptor)
				listClass.append(array(1).astype('float32'))
				lPos -= 1

		for pic in neg:
			neg_cuts = self.CUT.getPatches(pic)
			if lNeg == 0:
				break
			for p in neg_cuts:
				descriptor = self.HOG.getDescriptor(p)
				listSamples.append(descriptor)
				listClass.append(array(0).astype('float32'))
				lNeg -= 1

		return listSamples, listClass 

	# moze izrezati samo pozitive
	def getTestSamples(self, pos):
		listSamples = list()

		for pic in pos:
			pos_cuts = self.CUT.getPeople(pic[ 0 ], pic[ 1 ])
			for p in pos_cuts:
				descriptor = self.HOG.getDescriptor(p)
				listSamples.append(descriptor)
		return listSamples