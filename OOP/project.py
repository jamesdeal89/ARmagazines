"""This is the file for projecting the source object onto the webcam object"""
import numpy as np
import cv2
class Project():
    def __init__(self, webFrame,warpedSource,destinationPoints):
        self.webFrame = webFrame
        self.warpedSource = warpedSource
        self.destinationPoints = destinationPoints
    
    # the getter for webFrame
    @property
    def webFrame(self):
        return self._webFrame

    # the getter for warpedSource
    @property
    def warpedSource(self):
        return self._warpedSource

    # the getter for destinationPoints
    @property
    def destinationPoints(self):
        return self._destinationPoints

    # the setter for webFrame
    @webFrame.setter
    def webFrame(self,frame):
        self._webFrame = frame

    # the setter for warpedSource
    @warpedSource.setter
    def warpedSource(self,frame):
        self._warpedSource = frame
        self._homographyMatrix = matrix

    # the setter for destinationPoints
    @destinationPoints.setter
    def destinationPoints(self, points):
        self._destinationPoints = points
        self._dimensions = dimArray

    def project(self):
        """This method will use the intialized values for warpedSource and the webcamFrame
        to overlay the two and create an AR effect based on the destination points calculated via
        the Border() class"""
        # create a blank mask of 0s in the dimensions of the webcam frame
        self.mask2 = np.zeros(self.webFrame.shape, dtype=np.uint8)
        # create a white mask with a black box where the target was detected
        cv2.fillConvexPoly(self.mask2, self.destinationPoints, (255,255,255))
        self.mask2 = cv2.bitwise_not(self.mask2)
        self.masked_image2 = cv2.bitwise_and(self.webFrame, self.mask2)
        self.final = cv2.bitwise_and(self.webFrame,self.mask2)
        cv2.imshow("Ouput", self.final)
