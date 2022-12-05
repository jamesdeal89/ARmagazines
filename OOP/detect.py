"""This is the file for the detection class"""
class Detect():
    def __init__(self,webcam, targetsList):
        """
        Parameters:
        - webcam: the webcam object.
        - targetsList: array of target objects.
        """
        self.webcamFrame = webcam.frame
        self.targetsList = targetsList
        self.detected = None

    def detect(self):
        # Intialize the bruteforce matcher which scans entire webcam frame for keypoints of targets
        bruteForce = cv2.BFMatcher()
        # Iterate through each target object 
        for target in targetsList:
            ...