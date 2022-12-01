"""This is the file for projecting the source object onto the webcam object"""
class Project():
    def __init__(self, webFrame,warpedSource,destinationPoints):
        self.webFrame = webFrame
        self.warpedSource = warpedSource
        self.destinationPoints = destinationPoints
    
    # the getter for webFrame
    @property
    def webFrame(self):
        return self._webFrame

    # the getter for warpedSource
    @property
    def warpedSource(self):
        return self._warpedSource

    # the getter for destinationPoints
    @property
    def destinationPoints(self):
        return self._destinationPoints

    # the setter for webFrame
    @webFrame.setter
    def webFrame(self,frame):
        self._webFrame = frame

    # the setter for warpedSource
    @warpedSource.setter
    def warpedSource(self,frame):
        self._warpedSource = frame
        self._homographyMatrix = matrix

    # the setter for destinationPoints
    @destinationPoints.setter
    def destinationPoints(self, points):
        self._destinationPoints = points
        self._dimensions = dimArray

    def project(self):
        """This method will use the intialized values for warpedSource and the webcamFrame
        to overlay the two and create an AR effect based on the destination points calculated via
        the Border() class"""