"""This is file for the target class which inherits from the file class"""
import cv2
from file import File
class Target(File):
    """
    This is the Target class. It inherits from the File class. 
    It holds an OpenCV image object in it's attributes alongside
    it's keypoint data for later detection and recognition. 
    """
    def __init__(self, filepath, sourceObj):
        # Intialize the parent class, File using the filepath Parameter
        super().__init__(filepath)
        self._sourceObj = sourceObj

    # Method to generate the descriptors and keypoints
    def genPoints(self):
        orb = cv2.ORB_create(nfeatures=1000)
        # Create descriptor and keypoint attributes which can be used for target detection later
        self._keyPoints, self._descriptors = orb.detectAndCompute(self.getLoadedObj(),None)

    def getSourceObj(self):
        return self._sourceObj

    # getter for descriptors
    def getDescriptors(self):
        return self._descriptors

    # getter for keyPoints
    def getKeyPoints(self):
        return self._keyPoints

    def resize(self,w,h):
        self._loadedObj = cv2.resize(self._loadedObj,(w,h))