"""This is the file for the detection class"""
import cv2
import copy
import numpy as np 

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

    def detect(self):
        # Intialize the bruteforce matcher which scans entire webcam frame for keypoints of targets
        bruteForce = cv2.BFMatcher()
        # Iterate through each target object
        Matches = []
        for target in self.targetsList:
            print("CHECK......")
            self.webcam.genPoints()
            # Scan images to compare keypoints based on descriptors attributes
            matches = bruteForce.knnMatch(target.getDescriptors(),self.webcam.getDescriptors(),k=2)
            successfullMatches = []
            # Iterate through the matches and add them to a list of good matches if they're within a certain simiarity
            for targetMatch,sourceMatch in matches:
                if targetMatch.distance < 0.75 * sourceMatch.distance:
                    # Append the good match to a list
                    successfullMatches.append(targetMatch)
            Matches.append([successfullMatches, target])
        # Over 15 good matches will be considered a complete match
        for resultMatches in Matches:
            if len(resultMatches[0]) > 20:
                print("MATCHED")
                # If so, break the for loop and return the list of matches from the Detect method
                return resultMatches[0],resultMatches[1]

    
    def myHighPass(self,size,target):
        # size paramter limits how much of the image we filter and use
        # this can improve performance if image is high resolution
        # create a blank mask of empty zero values in size of sample
        """
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
        mask = np.zeros(shape=(size[1]+10,size[1]+10), dtype=np.float32)
        # create a deep copy of the target so that the original image is not affected, and change to grayscale
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY).astype(np.float32)
        # calculate the kernel for the 3x3 grid
        kernel = np.array([
                        [-1, -1, -1],
                        [-1,  8, -1],
                        [-1, -1, -1],], dtype=np.float32)
        # use OpenCV's filter2D function to convolve the kernel with the image to calculate the overall summed difference
        differential = cv2.filter2D(target_gray, -1, kernel, borderType=cv2.BORDER_CONSTANT)
        differential = differential[0:size[1]+10,0:size[1]+10]
        # if the overall difference with the surrounding pixels is greater than 60, adjust that pixel to be shown equal to how hard the edge is
        mask[differential > 50] = differential[differential > 50]
        # any values above 255 will be 'clipped' to make validating quality of samples better (see targets.myGenPoints)
        mask = np.clip(mask, 0, 255)
        # crop the mask to only show the sampled area
        mask = mask[size[0]:size[1],size[0]:size[1]]
        return mask


    def myDetect(self):
        """
        This class is intended to create my own implementation of OpenCV's image matcher and keypoint generator.
        My initial ideas are to use a 'high-pass' filter on the target images to only get B&W data on hard edges.
        This means that any colour variation caused by viewing the target through a webcam can be avoided.
        From this high-pass version, I will take the most significant keypoints by scanning over the image and then using the portions with high variety in pixels. These will be compared to scans across the target webcam frame to find the detected target. 
        """
        
        # create highpass of webcam --> convertScaleAbs makes it uniform absolute values for detection
        webcamHP = cv2.convertScaleAbs(self.myHighPass(size=[0,self.webcam.getFrame().shape[0]-10],target=self.webcam.getFrame()))

        cv2.imshow("HIGHPASS",webcamHP)
        # compare each section with details in each keypoint --> make keypoints small and vague, false positive is okay as we set a threshold anyways
        for target in self.targetsList:
            for sample in target.myGetPoints():
                # match the smaller sample we created to the template
                result = cv2.matchTemplate(webcamHP, sample, cv2.TM_CCOEFF_NORMED)

                threshold = 0.5
                # using a thershold accuracy we check where the match is similar enough
                locations = np.where(result >= threshold)

                # if we have more than 1 good match we return the detected target
                if len(locations[0]) > 0:
                    print("MY MATCHED")
                    return target









