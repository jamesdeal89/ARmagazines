"""This is the file for the detection class"""
import cv2
import copy
import sys
import numpy as np 
import imutils

class Detect():
    def __init__(self,webcam=None, targetsList=None):
        """
        Parameters:
        - webcam: the webcam object.
        - targetsList: array of target objects.
        """
        self.webcam = webcam
        self.targetsList = targetsList
        self.detected = None
        # generate the aruco dictionary for enhanced detection -> mostly for finding clean borders
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    @property
    def webcam(self):  
        return self._webcam
    
    @webcam.setter
    def webcam(self, webcam):
        self._webcam = webcam

    @property
    def targetsList(self):
        return self._targetsList
    
    @targetsList.setter
    def targetsList(self, targetsList):
        self._targetsList = targetsList
    
    @property
    def detected(self):
        return self._detected
    
    @detected.setter
    def detected(self, detected):
        self._detected = detected

    @property
    def arucoDict(self):
        return self._arucoDict
    
    @arucoDict.setter
    def arucoDict(self, arucoDict):
        self._arucoDict = arucoDict

    def detect(self):
        # Intialize the bruteforce matcher which scans entire webcam frame for keypoints of targets
        bruteForce = cv2.BFMatcher()
        self._webcam.genPoints()
        # Iterate through each target object
        Matches = []

        # check for aruco markers for more accurate borders
        arucoBorders = self.detectArucoMarkers()

        for target in self._targetsList:
            print("CHECK......"+ str(target._filepath) + str(len(target.getDescriptors())))
            # Scan images to compare keypoints based on descriptors attributes
            matches = bruteForce.knnMatch(target.getDescriptors(),self._webcam.getDescriptors(),k=2)
            successfullMatches = []
            # Iterate through the matches and add them to a list of good matches if they're within a certain simiarity
            for targetMatch,sourceMatch in matches:
                if targetMatch.distance < 0.75 * sourceMatch.distance:
                    # Append the good match to a list
                    successfullMatches.append(targetMatch)
            Matches.append([successfullMatches, target])
        # Over 15 good matches will be considered a complete match
        for resultMatches in Matches:
            print(str(len(resultMatches[0])) + str(resultMatches[1]._filepath))
            if len(resultMatches[0]) > 20:
                print("MATCHED", resultMatches[1]._filepath)
                # If so, break the for loop and return the list of matches from the Detect method alongside the detected target and, if applicable, the aruco marker borders
                return resultMatches[0], resultMatches[1], arucoBorders

    
    def myHighPass(self,size,target,threshold=80, x=0,y=0):
        # size paramter limits how much of the image we filter and use
        # this can improve performance if image is high resolution
        # create a blank mask of empty zero values in size of sample
        """
        if lowLevel:
            mask = np.zeros(shape=(size[1],size[1]))
            targetCOPY = copy.deepcopy(target)
            # change to greyscale
            target = cv2.cvtColor(targetCOPY, cv2.COLOR_BGR2GRAY)
            # iterate through each position in the empty matrix
            for i in range(size[0],size[1]):
                for j in range(size[0],size[1]):
                    # find the overall summed difference between the values in a 9*9 grid around the central current position
                    differential = -1*target[i][j]-1*target[i][j+1]-1*target[i][j+2]-1*target[i+1][j]+8*target[i+1][j+1]-1*target[i+1][j+2]-1*target[i+2][j]-target[i+2][j+1]-1*target[i+2][j+2]
                    
                    # if this overall differences with the surrounding pixels is greater than 80, we accept it as a hard edge and adjust that pixel to be shown equal to how hard the edge is.
                    if differential > 60:
                        mask[i][j] = differential
            # crop the mask to only show the sampled area
            mask = mask[size[0]:size[1],size[0]:size[1]]
            return mask
        """
        # create a blank mask of empty zero values in size of sample
        mask = np.zeros(shape=(size[1], size[0]), dtype=np.float32)
        # create a deep copy of the target so that the original image is not affected, and change to grayscale
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY).astype(np.float32)
        # calculate the kernel for the 3x3 grid
        kernel = np.array([
                        [-1, -1, -1],
                        [-1,  8, -1],
                        [-1, -1, -1],], dtype=np.float32)
        # select the target region based on the x and y coordinates
        target_region = target_gray[y:y+size[1], x:x+size[0]]
        # use OpenCV's filter2D function to convolve the kernel with the image to calculate the overall summed difference
        differential = cv2.filter2D(target_region, -1, kernel, borderType=cv2.BORDER_CONSTANT)
        # if the overall difference with the surrounding pixels is greater than the threshold value, adjust that pixel to be shown equal to how hard the edge is
        mask[differential > threshold] = differential[differential > threshold]
        # any values above 255 will be 'clipped' to make validating quality of samples better (see targets.myGenPoints)
        mask = np.clip(mask, 0, 255)
        return mask


    def myDetect(self):
        """
        This class is intended to create my own implementation of OpenCV's image matcher and keypoint generator.
        My initial ideas are to use a 'high-pass' filter on the target images to only get B&W data on hard edges.
        This means that any colour variation caused by viewing the target through a webcam can be avoided.
        From this high-pass version, I will take the most significant keypoints by scanning over the image and then using the portions with high variety in pixels. These will be compared to scans across the target webcam frame to find the detected target. 
        """


        # apply highpass filter to webcam image
        webcamHP = cv2.convertScaleAbs(self.myHighPass(size=[self._webcam.getFrame().shape[1]-10,self._webcam.getFrame().shape[0]-10],target=self._webcam.getFrame(), threshold=20))

        # Apply contrast normalization to image
        webcamHP = cv2.normalize(webcamHP, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        # Apply noise reduction to image
        webcamHP = cv2.GaussianBlur(webcamHP, (5, 5), 0)

        detectedTarget = None

        # rotate the target image by different angles and perform template matching on each rotated version
        for target in self._targetsList:
            print(str(target._filepath))
            for targetHP in target.myGetPoints():

                # Apply contrast normalization to image
                targetHP = cv2.normalize(targetHP, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

                # Apply noise reduction to image
                targetHP = cv2.GaussianBlur(targetHP, (5, 5), 0)

                scores = []
                angles = np.arange(0, 360, 5) # rotate by 5 degree increments
                for angle in angles:
                    rotated = imutils.rotate_bound(targetHP, angle) # rotate the image
                    result = cv2.matchTemplate(webcamHP, rotated, cv2.TM_CCOEFF_NORMED)
                    scores.append(np.max(result)) # store the maximum correlation score for each rotation

                # use the maximum score across all rotations as the final score for the template match
                max_score = np.max(scores)
                print(max_score)

                threshold = 0.29 # adjust threshold value

                # if the maximum score is above the threshold, return the location of the detected target
                if max_score >= threshold:
                    print("MY MATCHED")
                    detectedTarget = target  # return the target
            
        return detectedTarget 


    def detectArucoMarkers(self):
        """use opencv to detect aruco markers in the webcam frame"""
        # get the webcam frame
        frame = self._webcam.getFrame()
        # convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        parameters =  cv2.aruco.DetectorParameters()
        # detect aruco markers
        detector = cv2.aruco.ArucoDetector(self._arucoDict, parameters)
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
        # Check if all four markers are detected
        if ids is not None and len(ids) == 4:
            # Get the indices of the four markers
            marker_indices = np.where(np.isin(ids, [0, 1, 2, 3]))[0]
            # Extract the corner coordinates of the four markers
            marker_corners = np.array([corners[i][0] for i in marker_indices], dtype=np.float32)
            # return the corners of the markers -> this can help us remove need for border detetection
            return marker_corners
        # if we didn't detect an aruco marker, return None
        return None
