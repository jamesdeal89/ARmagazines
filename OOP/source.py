"""This is the class for source videos which inherits from the webcam class"""
from webcam import Webcam
import cv2
class Source(Webcam):
    """
    This is the Source class which inherits from the Webcam class.
    It similarly loads frames however from a file rather than a video capture device.
    """
    def __init__(self,filepath,autoText):
        # intialize the filepath from the parent class which is Webcam which then passes into that parent class which is File
        super().__init__(filepath=filepath)
        self.frame = None   
        self.autoText = autoText
    
    @property
    def frame(self):
        return self._frame
    
    @frame.setter
    def frame(self,frame):
        self._frame = frame
    
    @property
    def autoText(self):
        return self._autoText
    
    @autoText.setter
    def autoText(self,autoText):
        self._autoText = autoText

    # Getter for frame 
    def getFrame(self):
        return self._frame
    
    # Loads the video file - polymorphism of load() method in File/Webcam class
    def load(self):
        # Load the video file from the path and and assign to loadedVid attribute
        print(self.filepath)
        self._loadedVid = cv2.VideoCapture(self.filepath[0])
    
    # Loads the next frame of the video
    def next(self,w,h):
        # Here loadedBool is a True/False of whether the video has ended
        self._loadedBool, self._frame = self._loadedVid.read()
        self._frame = cv2.resize(self._frame,(w,h))
        if self._autoText:
            # add the detected OCR text onto the source frame
            # for each detected word
            for boxIndex in range(len(self._text['text'])):
                # get that word's detected location in x and y
                x,y = self._text['left'][boxIndex], self._text['top'][boxIndex]
                # insert text at that location with the same content
                cv2.putText(self._frame,self._text['text'][boxIndex],(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255))
        
    def setText(self,data):
        self._text = data