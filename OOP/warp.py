"""This file is for the warp class which takes a source object and warps it"""
import cv2
class Warp():
    def __init__(self, sourceFrame, homographyMatrix, dimensions):
        self._warpedImg = None
        self._homographyMatrix = homographyMatrix
        self._sourceFrame = sourceFrame
        self._dimensions = dimensions
    
    def warp(self):
        """
        Takes an image frame in the form of an OpenCV object.
        Warps the image by the provided homography matrix.
        Returns the resulting OpenCV object.
        """
        self._warpedImg = cv2.warpPerspective(self._sourceFrame, self._homographyMatrix, (self._dimensions[0],self._dimensions[1]))
        return self._warpedImg