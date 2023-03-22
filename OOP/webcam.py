"""This is the class for webcam objects which inherits from the file class"""
from file import File
import cv2
class Webcam(File):
    """
    This is the Webcam class which inherits from the File class
    """
    def __init__(self,filepath=None,lowRes=False):
        super().__init__(filepath)
        self._frame = None
        self._descriptors = None
        self._keyPoints = None
        self._loadedBool = None
        self._loadedWeb = None
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
            self._frame = cv2.resize(self._frame, (int(dimensions[1]*0.7), int(dimensions[0]*0.7)))

