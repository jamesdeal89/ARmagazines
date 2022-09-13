# first tutorial chapter for openCV 
import cv2

# images can be imported like so
img = cv2.imread('oldMan.jpeg', -1)
# there are several ways to process an image
# these include color, greyscale, and unchanged
# these are signified as:
# -1, cv2.IMREAD_COLOR
# 0, cv2.IMREAD_GREYSCALE
# 1, cv2.IMREAD_INCHANGED
# above I have put -1 as the second argument; meaning color

# images can be resized using cv2.resize and passing in a loaded image and a tuple for resolution
img = cv2.resize(img,(400,400))

cv2.imshow('image', img)
# waits for a keypress. 0 means infinitely, an integer means a sepcificed time until skipped
cv2.waitKey(0)
# closes all the windows made by cv2
cv2.destroyAllWindows()