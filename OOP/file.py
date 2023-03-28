"""The class for files as OpenCV objects"""
import cv2

class File():
    def __init__(self, filepath):
        self.filepath = filepath
        self._loadedObj = None
    
    # the getter for the filepath attribute
    @property
    def filepath(self):
        return self._filepath

    # the setter for the filepath attribute
    @filepath.setter
    def filepath(self,path):
        try: 
            # ensure the path isn't an invalid datatype
            int(path)
        except (TypeError, ValueError):
            self._filepath = path
            return True
        else:
            return False

    # getter for the loadedObj attribute
    def getLoadedObj(self):
        return self._loadedObj

    # loads the file from the filepath attribute and loads it as an OpenCV object, saved in the loadedObj attribute
    def load(self):
        self._loadedObj = cv2.imread(self.filepath)

