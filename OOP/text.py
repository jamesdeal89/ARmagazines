"""Class for extracting text from targets and adding them to source frames"""
import pytesseract
import cv2

class Text():
    def __init__(self, target):
        self._target = target

    def process(self):
        self._processedTarget = cv2.cvtColor(self._target.getLoadedObj(), cv2.COLOR_BGR2GRAY)
        #self._processedTarget = cv2.threshold(self._processedTarget, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    def extract(self):
        # this image_to_date returns a dictionary. The key of the dictionary is the text detected and the data includes:
        # location co-ordinates and confidence scores --> this can be used later to relicate this text in the same location on the source frame
        data = pytesseract.image_to_data(self._processedTarget, output_type=pytesseract.Output.DICT)
        self._data = data

    def addText(self):
        self._target.getSourceObj().setText(self._data)
