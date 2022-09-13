# using https://medium.com/acmvit/how-to-project-an-image-in-perspective-view-of-a-background-image-opencv-python-d101bdf966bc
import cv2
import numpy

sourcePoints = numpy.array([[0,0],[800,0],[0,1042],[800,1042]])
targetPoints = numpy.array([[125,188],[372,144],[414,610],[650,482]])
source = cv2.imread("source.jpeg")
target = cv2.imread("target.jpeg")


# cv2.findHomography() will return a homography matrix and a mask as a tuple
# it takes in four arguments:
# a list of the source coordinates, a list of the target coordinates, the method, maximum allowed reporjection error
# there are four method options:
# 0 - regular method using all points
# cv2.RANSAC 
# cv2.LMEDS 
# cv2.RHO 
homographyMatrix, mask = cv2.findHomography(sourcePoints, targetPoints, cv2.RANSAC, 5.0)
print(homographyMatrix)


# cv2.warpPerspective() can be used to warp images
# it takes these three inputs:
# the source image, a homography matrix, and the target image's width and height
warpedSource = cv2.warpPerspective(source,homographyMatrix,(1200,627))
while True:
    cv2.imshow("warped image",warpedSource)