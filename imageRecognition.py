# resources used:
# https://learnopencv.com/image-alignment-feature-based-using-opencv-c-python/
# https://youtu.be/7gSWd2hodFU
# https://youtu.be/oXlwWbU8l2o
import cv2

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
        # this a built in cv2 function which shows a drawn line of matched features parralel to each other
        features = cv2.drawMatches(target,keyPoints,webFrame,keyPointsWeb,successfullMatches,None,flags=2)
        cv2.imshow("features", features)
    elif len(successfullMatches2) > 20:
        # this a built in cv2 function which shows a drawn line of matched features parralel to each other
        features = cv2.drawMatches(target2,keyPoints2,webFrame,keyPointsWeb,successfullMatches2,None,flags=2)
        cv2.imshow("features", features)
    elif len(successfullMatches3) > 20:
        # this a built in cv2 function which shows a drawn line of matched features parralel to each other
        features = cv2.drawMatches(target3,keyPoints3,webFrame,keyPointsWeb,successfullMatches3,None,flags=2)
        cv2.imshow("features", features)

    # wait for keypress and if keypress is q or Q, break loop
    buttonPress = cv2.waitKey(1)
    if buttonPress==81 or buttonPress==113:
        break

feed.release()

