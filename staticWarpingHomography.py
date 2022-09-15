# using https://medium.com/acmvit/how-to-project-an-image-in-perspective-view-of-a-background-image-opencv-python-d101bdf966bc
import cv2
import numpy

sourcePoints = numpy.array([[0,0],[800,0],[0,1042],[800,1042]])
targetPoints = numpy.array([[125,188],[372,144],[414,610],[650,482]])
source = cv2.imread("source.jpg",-1)
target = cv2.imread("target.jpg",-1)


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

# display the warped source not overlain yet
cv2.imshow("warped image",warpedSource)
cv2.waitKey(0)

# blend the two images and display them
overlay = cv2.addWeighted(target,0.5,warpedSource,0.5,0.0)
cv2.imshow("overlaid images", overlay)
cv2.waitKey(0)

# black mask of target
mask2 = numpy.zeros((627,1200),dtype=numpy.uint8)
cv2.imshow("combining", mask2)
cv2.waitKey(0)
targetPoints = numpy.array([[372,144],[125,188],[414,610],[650,482]])
# fill mask with white area of warped source
mask2 = cv2.fillConvexPoly(mask2,targetPoints,(255,255,255))
cv2.imshow("combining", mask2)
cv2.waitKey(0)
mask2 = cv2.bitwise_not(mask2)
cv2.imshow("combining", mask2)
cv2.waitKey(0)
mask2 = cv2.bitwise_and(target, mask2)
cv2.imshow("combining", mask2)
cv2.waitKey(0)
finalOutput = cv2bitwise_or(warpedSource,mask2)

cv2.imshow("final", finalOutput)
cv2.waitKey(0)

