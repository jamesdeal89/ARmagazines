"""
For this iteration I want to add a comand line interface to make loading target magazine covers and source
videos more user friendly. I want to progress this further by using Tkinter to make a full GUI.
Additionally I think it's important to allow for more than 3 targets/sources and that will require using
file I/O to store and loops to iterate through the saved locations and make variables for each.
Further functionalisation of my code may be required to make using infinitely more targets possible.
"""
import sys
import cv2
import numpy as np
import csv
import re
import os

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

    # flip the image to make the target area black (0) and the rest white (1)
    mask2 = cv2.bitwise_not(mask2)

    # using a bitwise and to mask over the area in the webcam which holds the target
    # this works as the mask is white (1) in areas which don't contain the target.
    # therefore an AND operation with the webcam data which is also 1's and 0's.
    # will just maintain the webcam data as A.1 = A
    # whereas the target area is black (0) so if we do A.0 it simplifies to 0
    # leaving the target area as all 0 values. 
    masked_image2 = cv2.bitwise_and(webFrame, mask2)
    # using bitwise or to merge the two images
    final = cv2.bitwise_or(warpedSource, masked_image2)

    # displaying each stage for documentation purposes
    cv2.imshow("mask", mask2)
    cv2.imshow("masked_image2", masked_image2)
    cv2.imshow("overlay", final)
    cv2.imshow("warped source", warpedSource)


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
    if len(successfullMatches) > 15:
        return successfullMatches, 1
    elif len(successfullMatches2) > 15:
        return successfullMatches2, 2
    elif len(successfullMatches3) > 15:
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


def generateCSV(pairings, createOrUpdate):
    # this will use file I/O and the csv library to take the pairing dictionary list and either write or append to 
    # a pairs.csv file.
    with open("pairs.csv",createOrUpdate) as file:
        # use the csv library's dictionary writer to make the .csv file's heading (if creating) and for later writing each dict
        dictwriter = csv.DictWriter(file, fieldnames=pairings[0].keys())
        if createOrUpdate == "w":
            dictwriter.writeheader()
        # iterate through the pairs list to get each dictionary 
        for pair in pairings:
            dictwriter.writerow(pair)


def generatePairs(createOrUpdate):
    # create a csv file of the target and source pairs if one does not exist
    # allow user to keep entering target and source pair filenames with .mp4 and .jpeg images until ctrl+D
    # verify input using regex
    targetSource = []
    print("This entry will continue for more pairs until ctrl+D is pressed")
    while True:
        try:
            pairing = {}
            pair = input("Please input your target filename (.jpeg/.jpg) followed by source filename (.mp4) as such: 'target.jpg, source.jpg':")
            # use regex to ensure the user has used the correct syntax for input and use regex groupings to capture the data we want
            if matches := re.search(r"^(.+), (.+)",pair):
                fileTarget = matches.group(1)
                fileSource = matches.group(2)
                # seperate the file extensions using os library 
                name,ext = os.path.splitext(fileTarget)
                name1,ext1 = os.path.splitext(fileSource)
                # check that both file extensions are valid to avoid OpenCV compatability errors
                if ext in [".jpg",".jpeg"] and ext1 == ".mp4":
                    # if valid update the dictionary pair and append it to the list
                    pairing["target"] = fileTarget
                    pairing["source"] = fileSource
                    targetSource.append(pairing)
                else:
                    print("\n\nfile extension not compatible")
            else:
                print("\n\nPlease use the format of 'targetFile, sourceFile' including extensions")
        except EOFError:
            # if ctrl+D is pressed break the entry loop
            print("\n\nYou have pressed ctrl+D and have completed entry.")
            print("Your pairings are below:")
            print(targetSource)
            break
    # once loop is broken we call the file generator function
    generateCSV(targetSource,createOrUpdate)
        


def loadPairs():
    # use a csv file to load the target and source pairs using loops
    # after this the loaded pairs will be passed into a function which uses OpenCV and iterative loops
    # to load all the pairs into OpenCV image objects.
    with open("pairs.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            ...


def main():
    while True:
        loadOrGen = input("Do you want to load, generate, or update a target-source pair file? (L,G, or U)").strip().lower()
        if loadOrGen == "l":
            try:
                loadPairs()
            except FileNotFoundError:
                # catch any error where the file pairs.csv does not exist and exit while giving error message
                sys.exit("There was no pairs.csv file found in the local directory. File must be named pairs.csv to load.")
            else:
                # if the pair loading was successful we can break the loop for checking input
                break
        elif loadOrGen == "g":
            # call the generate function and pass in "w" to create or overwrite a pairs.csv file
            generatePairs("w")
            break
        elif loadOrGen == "u":
            # using the same generate function except pass in "a" to append to an already exisiting pairs.csv file
            generatePairs("a")
            break

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