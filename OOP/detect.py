"""This is the file for the detection class"""
import cv2
class Detect():
    def __init__(self,webcam, targetsList):
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
        print(self.targetsList) 
        Matches = []
        for target in self.targetsList:
            print("CHECK......")
            # load and create keypoints+descriptors for each target object using it's methods
            target.genPoints()
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
            if len(resultMatches[0]) > 15:
                print("MATCHED")
                # If so, break the for loop and return the list of matches and the matched target object from the Detect method
                return resultMatches[0], resultMatches[1]
