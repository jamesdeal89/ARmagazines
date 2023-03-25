"""Class for extracting text from targets and adding them to source frames"""
import pytesseract
import cv2
import numpy as np

class Text():
    def __init__(self, target):
        self._target = target

    def greyscale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def thresholding(self,image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def opening(self,image):
        # processing method to improve OCR accuracy 
        kernel = np.ones((5,5),np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    def process(self):
        # convert to B&W and then apply above method for 'opening' filter
        self._processedTarget = self.greyscale(self._target.getLoadedObj())
        self._processedTarget = self.thresholding(self._processedTarget)

    def extract(self):
        # this image_to_date returns a dictionary. The key of the dictionary is the text detected and the data includes:
        # location co-ordinates and confidence scores --> this can be used later to relicate this text in the same location on the source frame
        data = pytesseract.image_to_data(self._processedTarget, output_type=pytesseract.Output.DICT)
        self._data = data

    def addText(self):
        self._target.getSourceObj().setText(self._data)
