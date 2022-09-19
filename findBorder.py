# written using my sources in my bibliography
# specifically https://docs.opencv.org/3.4/d9/dab/tutorial_homography.html
# also using the base code from the imageRecognition.py and thus the sources of that file
# focus for this file is finding border coordinates to later project and warp the source
# resources used:
# https://learnopencv.com/image-alignment-feature-based-using-opencv-c-python/
# https://youtu.be/7gSWd2hodFU
# https://youtu.be/oXlwWbU8l2o
# I understand the code is messy and procedures would reduce unecesary complexity by a lot
# but first I want to create a proof of concept and then clean up the implementation after

import cv2
import numpy as np

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

# get the first frame of the source. If it fails the source will stop being read
read, frame = source.read()

# resizing all targets and source to be the same
# .shape on a loaded image returns a tuple of height, width, and channels
h, w, c = target.shape
frame = cv2.resize(frame,(w,h))
target2 = cv2.resize(target2,(w,h))
target3 = cv2.resize(target3,(w,h))

# using cv2 ORB which is a feature which creates image alignment detectors
# nfeatures specifices the number of features to use as matching points
orb = cv2.ORB_create(nfeatures=1000)
keyPoints, descriptors = orb.detectAndCompute(target,None)
# displays our keypoints for documentation purposes
# target = cv2.drawKeypoints(target,keyPoints,None)
# creating two more orb keypoints for the other two targets
keyPoints2, descriptors2 = orb.detectAndCompute(target2,None)
keyPoints3, descriptors3 = orb.detectAndCompute(target3,None)


# read the webcam in a loop
while True:
    webRead, webFrame = feed.read()
    # read the keypoints in the orb of the webcam frames
    # we can use these to compare to the target keypoints
    keyPointsWeb, descriptorsWeb = orb.detectAndCompute(webFrame,None)
    # display webcam keypoints for documentation 
    # webFrame = cv2.drawKeypoints(webFrame, keyPointsWeb,None)
    bruteForce = cv2.BFMatcher()
    matches = bruteForce.knnMatch(descriptors,descriptorsWeb, k=2)
    matches2 = bruteForce.knnMatch(descriptors2,descriptorsWeb, k=2)
    matches3 = bruteForce.knnMatch(descriptors3,descriptorsWeb, k=2)
    successfullMatches = []
    successfullMatches2 = []
    successfullMatches3 = []
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
    
    # for testing to check number of good matches
    print(len(successfullMatches))
    
    if len(successfullMatches) > 20: 
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
        sourcePoints = np.float32([[0,0],[0,h],[w,h],[w,0]]).reshape(-1,1,2)

        # now we warp those border points based on where cv2 thinks it's found the same points through the webcam
        # this is done using the homography matrix
        destinationPoints = cv2.perspectiveTransform(sourcePoints,homographyMatrix)
        # we now add these border lines of the target image to the webcam frame
        cv2.polylines(webFrame,[np.int32(destinationPoints)],True,(255,255,255),3)


        # this a built in cv2 function which shows a drawn line of matched features parralel to each other
        features = cv2.drawMatches(target,keyPoints,webFrame,keyPointsWeb,successfullMatches,None,flags=2)
        cv2.imshow("features", features)
    elif len(successfullMatches2) > 20:
        originalPoints = np.float32([keyPoints2[m.queryIdx].pt for m in successfullMatches2]).reshape(-1,1,2)
        destinationPoints = np.float32([keyPointsWeb[m.trainIdx].pt for m in successfullMatches2]).reshape(-1,1,2)
        homographyMatrix, mask = cv2.findHomography(originalPoints,destinationPoints,cv2.RANSAC,5)
        # we now create the base frame of the source which is just the dimenions of the image
        # we calculated this previously so I'll just pass in the variables.
        sourcePoints = np.float32([[0,0],[0,h],[w,h],[w,0]]).reshape(-1,1,2)

        # now we warp those border points based on where cv2 thinks it's found the same points through the webcam
        # this is done using the homography matrix
        destinationPoints = cv2.perspectiveTransform(sourcePoints,homographyMatrix)
        # we now add these border lines of the target image to the webcam frame
        cv2.polylines(webFrame,[np.int32(destinationPoints)],True,(255,255,255),3)
        # this a built in cv2 function which shows a drawn line of matched features parralel to each other
        features = cv2.drawMatches(target2,keyPoints2,webFrame,keyPointsWeb,successfullMatches2,None,flags=2)
        cv2.imshow("features", features)
    elif len(successfullMatches3) > 20:
        originalPoints = np.float32([keyPoints3[m.queryIdx].pt for m in successfullMatches3]).reshape(-1,1,2)
        destinationPoints = np.float32([keyPointsWeb[m.trainIdx].pt for m in successfullMatches3]).reshape(-1,1,2)
        homographyMatrix, mask = cv2.findHomography(originalPoints,destinationPoints,cv2.RANSAC,5)
        # we now create the base frame of the source which is just the dimenions of the image
        # we calculated this previously so I'll just pass in the variables.
        sourcePoints = np.float32([[0,0],[0,h],[w,h],[w,0]]).reshape(-1,1,2)

        # now we warp those border points based on where cv2 thinks it's found the same points through the webcam
        # this is done using the homography matrix
        destinationPoints = cv2.perspectiveTransform(sourcePoints,homographyMatrix)
        # we now add these border lines of the target image to the webcam frame
        cv2.polylines(webFrame,[np.int32(destinationPoints)],True,(255,255,255),3)
        # this a built in cv2 function which shows a drawn line of matched features parralel to each other
        features = cv2.drawMatches(target3,keyPoints3,webFrame,keyPointsWeb,successfullMatches3,None,flags=2)
        cv2.imshow("features", features)

    # wait for keypress and if keypress is q or Q, break loop
    buttonPress = cv2.waitKey(1)
    if buttonPress==81 or buttonPress==113:
        break

feed.release()

