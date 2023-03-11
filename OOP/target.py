"""This is file for the target class which inherits from the file class"""
import cv2
from file import File
from detect import Detect
import numpy as np
import copy

class Target(File):
    """
    This is the Target class. It inherits from the File class. 
    It holds an OpenCV image object in it's attributes alongside
    it's keypoint data for later detection and recognition. 
    """
    def __init__(self, filepath, sourceObj):
        # Intialize the parent class, File using the filepath Parameter
        super().__init__(filepath)
        self._sourceObj = sourceObj
        self._myPoints = [None]

    # Method to generate the descriptors and keypoints
    def genPoints(self):
        orb = cv2.ORB_create(nfeatures=1000)
        # Create descriptor and keypoint attributes which can be used for target detection later
        self._keyPoints, self._descriptors = orb.detectAndCompute(self.getLoadedObj(),None)

    def myGetPoints(self):
        return self._myPoints

    def mySetPoints(self,sample):
        # Using my own implementation of image detection which can be used when in 'performance' mode.
        self._myPoints.append(sample)
    
    def myGenPoints(self):
        # generates keypoints using my own implementation in Detect class
        # this also ensures that the samples generated have enough features within them using .sum()
        detect = Detect()
        sum_of_pixels = 0
        # this holds previous samples, if we fail to get a good match, we take this next best choice
        previous = {}
        position = 100 
        h,w,c = self.getLoadedObj().shape
        while sum_of_pixels < 150000:
            # prevent going over edge of image
            if position + 99 > w:
                # if we go over edge, take the best previous sample
                key = max(previous.keys())
                self._myPoints[0] = previous[key]
                break
            self._myPoints[0] = cv2.convertScaleAbs(detect.myHighPass(size=[position,100+position],target=self.getLoadedObj()))
            sum_of_pixels = np.sum(self._myPoints[0])
            cv2.imshow("parsing",self._myPoints[0])
            cv2.waitKey(0)
            # save the current sample incase we overrun
            previous[sum_of_pixels] = copy.deepcopy(self._myPoints[0])
            # move our parse
            position += 100
        cv2.imshow("sample gen", self._myPoints[0])
        cv2.waitKey(0)
    
    def myGetPoints(self):
        return self._myPoints

    def getSourceObj(self):
        return self._sourceObj

    # getter for descriptors
    def getDescriptors(self):
        return self._descriptors

    # getter for keyPoints
    def getKeyPoints(self):
        return self._keyPoints

    def resize(self,w,h):
        self._loadedObj = cv2.resize(self._loadedObj,(w,h))

