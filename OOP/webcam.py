"""This is the class for webcam objects which inherits from the file class"""
from file import File
import cv2
import copy

class Webcam(File):
    """
    This is the Webcam class which inherits from the File class
    """
    def __init__(self,filepath=None,lowRes=False):
        super().__init__(copy.deepcopy(filepath))
        self.frame = None
        self.descriptors = None
        self.keyPoints = None
        self.loadedBool = None
        self.loadedWeb = None
        self.lowRes = lowRes

    @property
    def frame(self):
        return self._frame
    
    @frame.setter
    def frame(self,frame):
        self._frame = frame
    
    @property
    def descriptors(self):
        return self._descriptors
    
    @descriptors.setter
    def descriptors(self,descriptors):
        self._descriptors = descriptors

    @property
    def keyPoints(self):
        return self._keyPoints
    
    @keyPoints.setter
    def keyPoints(self,keyPoints):
        self._keyPoints = keyPoints

    @property
    def loadedBool(self):
        return self._loadedBool
    
    @loadedBool.setter
    def loadedBool(self,loadedBool):
        self._loadedBool = loadedBool
    
    @property
    def loadedWeb(self):
        return self._loadedWeb
    
    @loadedWeb.setter
    def loadedWeb(self,loadedWeb):
        self._loadedWeb = loadedWeb

    @property
    def lowRes(self):
        return self._lowRes
    
    @lowRes.setter
    def lowRes(self,lowRes):
        self._lowRes = lowRes

    # Method to generate the descriptors and keypoints
    def genPoints(self):
        orb = cv2.ORB_create(nfeatures=1000)
        # Create descriptor and keypoint attributes which can be used for target detection later
        self._keyPoints, self._descriptors = orb.detectAndCompute(self._frame,None)

    # Getter for descriptors
    def getDescriptors(self):
        return self._descriptors

    # Getter for keyPoints
    def getKeyPoints(self):
        return self._keyPoints

    # Getter for frame 
    def getFrame(self):
        return self._frame

    # Loads the webcam feed - polymorphism of load() method in File class
    def load(self):
        # Load the default webcam feed and assign to loadedWeb attribute
        self._loadedWeb = cv2.VideoCapture(0)

    # Loads the next frame of the webcam
    def next(self):
        # Here loadedBool is a True/False of whether the feed is ended
        self._loadedBool, self._frame = self._loadedWeb.read()
        dimensions = self._frame.shape
        if self._lowRes:
            # Resize the image to increase framerate
            self._frame = cv2.resize(self._frame, (int(dimensions[1]*self._lowRes), int(dimensions[0]*self._lowRes)))
        

