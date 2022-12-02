"""This file is for the warp class which takes a source object and warps it"""
import cv2
class Warp():
    def __init__(self, sourceFrame, homographyMatrix, dimensions):
        self.warpedImg = None
        self.homographyMatrix = homographyMatrix
        self.sourceFrame = sourceFrame
        self.dimensions = dimensions
    
    @property
    def warpedImg(self):
        return self._warpedImg

    @property
    def homographyMatrix(self):
        return self._homographyMatrix

    @property
    def sourceFrame(self):
        return self._sourceFrame

    @property
    def dimenions(self):
        return self._dimensions

    @warpedImg.setter
    def warpedImg(self,img):
        self._warpedImg = img

    @homographyMatrix.setter
    def homographyMatrix(self,matrix):
        self._homographyMatrix = matrix

    @sourceFrame.setter
    def sourceFrame(self,frame):
        self._sourceFrame = frame

    @dimensions.setter
    def dimesnions(self,list):
        self._dimensions = list

    def warp(self):
        """
        Takes an image frame in the form of an OpenCV object.
        Warps the image by the provided homography matrix.
        Returns the resulting OpenCV object.
        """
        self._warpedImg = cv2.warpPerspective(self._sourceFrame, self._homographyMatrix, (self._dimensions[0],self._dimensions[1]))
        return self._warpedImg