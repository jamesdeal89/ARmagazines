"""
To start with this file, I want to clean up the previous implementation
then I want to use my knowledge of perspective warping to frame by frame
adjust the source video to fit onto the target through the webcam.
To improve efficiency I'll start by making procedures and functions.
Then after finishing my proof of concept I'll create an OOP structure and make my 
own implementation of cv2 based algorithms.
"""
import sys
import cv2
import numpy as np

def overlay(webFrame, sourceFrame, target, homographyMatrix, destinationPoints,w,h):
    # we take the warped source frame and the webcam frame and overlay the two
    # this is done using masks of black and white and using AND/XOR operators 
    # this as as we can delete the sections over the detected target with the AND
    # as if one is a white (1) mask and one is black (0) they will result in a 0 result
    # and then use the XOR to overlay the source onto that area as it will use the positive
    # source bits over the negative black area where the target was.

    # warp the source frame by the homography we calcuated 
    warpedSource = cv2.warpPerspective(sourceFrame, homographyMatrix, (w,h))
    # create a blank mask of 0s in the dimensions of the webcam frame
    mask2 = np.zeros(webFrame.shape, dtype=np.uint8)
    # create a white mask with a black box where the target was detected
    cv2.fillConvexPoly(mask2, destinationPoints, (255,255,255))

    
    mask2 = cv2.bitwise_not(mask2)

    print(webFrame.shape)
    print(mask2.shape)
    print(destinationPoints.shape)

    masked_image2 = cv2.bitwise_and(webFrame, mask2)
    cv2.imshow("masked image", masked_image2)

    #Using Bitwise or to merge the two images
    final = cv2.bitwise_or(warpedSource, masked_image2)
    cv2.imshow("mask", mask2)
    cv2.imshow("web", webFrame)
    cv2.imshow("source", sourceFrame)
    cv2.imshow("overlay", final)


def findBorder(webFrame,target, sourceFrame,w,h, orb, keyPointsWeb,keyPoints,successfullMatches):
    print("finding border")
    # we need to reformat the data in the successful matches to allow us to put it into cv2.findHomography 
    # this is done using numpy's .reshape and a numpy array
    # we pass in -1, 1, 2 as we want 1 array with 2 elements each conatined within whatever it's divisible into
    # thus the -1 which means numpy will calculate the value for us.
    originalPoints = np.float32([keyPoints[m.queryIdx].pt for m in successfullMatches]).reshape(-1,1,2)
    destinationPoints = np.float32([keyPointsWeb[m.trainIdx].pt for m in successfullMatches]).reshape(-1,1,2)
    # then we put the reformatted arrays of points into cv2.findHomography
    # we do this to find the difference between the points in the source and the one we see through the camera
    # based on how different they are based on distance, we find a homography matrix which can be used to distort 
    # a source video into the same perspective as the real life target. 
    # we're using cv2's RANSAC method of calculation
    homographyMatrix, mask = cv2.findHomography(originalPoints,destinationPoints,cv2.RANSAC,5)
    
    # we now create the base frame of the source which is just the dimenions of the image
    # we calculated this previously so I'll just pass in the variables.
    sourcePoints = np.float32([[0,0],[w1,0],[w1,h1],[0,h1]]).reshape(-1,1,2)

    # now we warp those border points based on where cv2 thinks it's found the same points through the webcam
    # this is done using the homography matrix
    destinationPoints = cv2.perspectiveTransform(sourcePoints,homographyMatrix)
    # we now add these border lines of the target image to the webcam frame
    #cv2.polylines(webFrame,[np.int32(destinationPoints)],True,(255,255,255),3)

    # this a built in cv2 function which shows a drawn line of matched features parralel to each other
    # features = cv2.drawMatches(target,keyPoints,webFrame,keyPointsWeb,successfullMatches,None,flags=2)
    # print("showing frame")
    # cv2.imshow("features", features)

    overlay(webFrame, sourceFrame, target, homographyMatrix, np.int32(destinationPoints), w, h)


def recognizeCover(webFrame, descriptors, descriptors2, descriptors3, descriptorsWeb):
    print("looking for cover")
    # using a bruteforce method of scanning across the entire image for the keypoints
    bruteForce = cv2.BFMatcher()
    matches = bruteForce.knnMatch(descriptors,descriptorsWeb, k=2)
    matches2 = bruteForce.knnMatch(descriptors2,descriptorsWeb, k=2)
    matches3 = bruteForce.knnMatch(descriptors3,descriptorsWeb, k=2)
    # lists to store data on the matched keypoints later 
    successfullMatches = []
    successfullMatches2 = []
    successfullMatches3 = []
    # loops which only add to the successfull matches lists if it's within a certain allowance of variation from the original keypoint
    for targetMatch,sourceMatch in matches:
        # find the distance and accept is less than 0.75 off
        if targetMatch.distance < 0.75 * sourceMatch.distance:
            # add the good matches to the list
            successfullMatches.append(targetMatch)
    for targetMatch,sourceMatch in matches2:
        # find the distance and accept is less than 0.75 off
        if targetMatch.distance < 0.75 * sourceMatch.distance:
            # add the good matches to the list
            successfullMatches2.append(targetMatch)
    for targetMatch,sourceMatch in matches3:
        # find the distance and accept is less than 0.75 off
        if targetMatch.distance < 0.75 * sourceMatch.distance:
            # add the good matches to the list
            successfullMatches3.append(targetMatch)
    # if there are more than 20 matches we assume it's a positive match 
    # and return which magazine it is using an integer code alongside the keypoints matched in a tuple
    if len(successfullMatches) > 17:
        return successfullMatches, 1
    elif len(successfullMatches2) > 17:
        return successfullMatches2, 2
    elif len(successfullMatches3) > 17:
        return successfullMatches3, 3
    else:
        return None, None


def webcamRead(feed, source,target, target2, target3, orb, keyPoints, keyPoints2, keyPoints3, descriptors, descriptors2, descriptors3):
    global h1,w1,c1
    frameLoaded, webFrame = feed.read()
    sourceLoaded, sourceFrame = source.read()
    print("reading webcam")
    while frameLoaded and sourceLoaded:

        # read the keypoints in the orb of the webcam frames
        # we can use these to compare to the target keypoints
        keyPointsWeb, descriptorsWeb = orb.detectAndCompute(webFrame,None)

        # find which magazine is in the webcam and store the matching points (later used for creating a homography matrix)
        matches, targetNum = recognizeCover(webFrame, descriptors, descriptors2, descriptors3, descriptorsWeb)

        h, w, c = webFrame.shape
        h1, w1, c1 = target.shape

        # resizing all targets and source to be the same
        # .shape on a loaded image returns a tuple of height, width, and channels
        target2 = cv2.resize(target2,(w1,h1))
        target3 = cv2.resize(target3,(w1,h1))
        sourceFrame = cv2.resize(sourceFrame,(w1,h1))
        # wait for keypress and if keypress is q or Q, break loop

        # find the border of the target image found through the webcam based on which target cover it is
        if targetNum != None:
            if targetNum == 1:
                findBorder(webFrame,target,sourceFrame, w,h, orb, keyPointsWeb,keyPoints,matches)
            elif targetNum == 2:
                findBorder(webFrame, target2,sourceFrame, w,h, orb, keyPointsWeb,keyPoints2,matches)
            elif targetNum == 3:
                findBorder(webFrame, target3,sourceFrame, w,h, orb, keyPointsWeb,keyPoints3,matches)



        # load the next frame and update boolean
        frameLoaded, webFrame = feed.read()
        sourceLoaded, sourceFrame = source.read()

        buttonPress = cv2.waitKey(1)
        if buttonPress==81 or buttonPress==113:
            sys.exit()


def main():
    # get default webcam feed
    feed = cv2.VideoCapture(0)
    # load target image to detect and map onto (ignore filename)
    target = cv2.imread("target.jpg")
    # load secondary image target
    target2 = cv2.imread("target2.jpg")
    # load third image 
    target3 = cv2.imread("target3.jpg")
    # load source video to project onto the target
    source = cv2.VideoCapture("source.mp4")



    # using cv2 ORB which is a feature which creates image detector keypoints
    # nfeatures specifices the number of features to use as matching points
    # positioning relationships and arrangements of pixels are used
    orb = cv2.ORB_create(nfeatures=1000)
    keyPoints, descriptors = orb.detectAndCompute(target,None)
    # displays our keypoints for documentation purposes
    # target = cv2.drawKeypoints(target,keyPoints,None)
    # creating two more orb keypoints for the other two targets
    keyPoints2, descriptors2 = orb.detectAndCompute(target2,None)
    keyPoints3, descriptors3 = orb.detectAndCompute(target3,None)

    webcamRead(feed, source, target, target2, target3, orb,keyPoints, keyPoints2, keyPoints3, descriptors, descriptors2, descriptors3)


if __name__ == "__main__":
    main()