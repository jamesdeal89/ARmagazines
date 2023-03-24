# the file for the class Border which finds the borders of the detected target in the webcam frame
import cv2
import numpy as np
class Border():
    def __init__(self, target, webcam, successfullMatches, arucoBorders):
        self._target = target
        self._webcam = webcam
        self._successfullMatches = successfullMatches
        self._arucoBorders = arucoBorders

    def border(self):
        h1,w1,c1 = self._target.getLoadedObj().shape
        sourcePoints = np.float32([[0,0],[w1,0],[w1,h1],[0,h1]]).reshape(-1,1,2)

        if self._arucoBorders is None:
            originalPoints = np.float32([self._target.getKeyPoints()[m.queryIdx].pt for m in self._successfullMatches]).reshape(-1,1,2)
            destinationPoints = np.float32([self._webcam.getKeyPoints()[m.trainIdx].pt for m in self._successfullMatches]).reshape(-1,1,2)
        else:
            # if we did detect an aruco marker we can use that to calculate homography rather than keypoints
            originalPoints = sourcePoints
            destinationPoints = self._arucoBorders
        
        homographyMatrix, mask = cv2.findHomography(originalPoints,destinationPoints,cv2.RANSAC,5)

        try:
            destinationPoints = cv2.perspectiveTransform(sourcePoints, homographyMatrix)
        except cv2.error:
            # if we hit CV2 error it means we had a false match and we can catch this error
            return

        return destinationPoints, homographyMatrix