"""The class for files as OpenCV objects"""
import cv2
class File():
    def __init__(self, filepath):
        self.filepath = filepath
        self._loadedObj = None
    
    # the setter for the filepath attribute
    @filepath.setter
    def filepath(self,path):
        try: 
            # ensure the path isn't an invalid datatype
            int(path)
        except TypeError:
            self._filepath = path
            return True
        else:
            return False

    # the getter for the filepath attribute
    @property
    def filepath(self):
        return self._filepath
    
    # getter for the loadedObj attribute
    def getLoadedObj(self):
        return self._loadedObj

    # loads the file from the filepath attribute and loads it as an OpenCV object, saved in the loadedObj attribute
    def load(self):
        self._loadedObj = OpenCV.imread(self.filepath)

