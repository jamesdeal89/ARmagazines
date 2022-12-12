"""This is the class for source videos which inherits from the webcam class"""
from webcam import Webcam
import cv2
class Source(Webcam):
    """
    This is the Source class which inherits from the Webcam class.
    It similarly loads frames however from a file rather than a video capture device.
    """
    def __init__(self, filepath):
        # intialize the filepath from the parent class which is Webcam which then passes into that parent class which is File
        super().__init__(filepath=filepath)
        self._frame = None   
    
    # Getter for frame 
    def getFrame(self):
        return self._frame
    
    # Loads the video file - polymorphism of load() method in File/Webcam class
    def load(self):
        # Load the video file from the path and and assign to loadedVid attribute
        print(self.filepath)
        self._loadedVid = cv2.VideoCapture(self.filepath[0])
    
    # Loads the next frame of the video
    def next(self):
        # Here loadedBool is a True/False of whether the video has ended
        self._loadedBool, self._frame = self._loadedVid.read()