# done using tutorial from https://youtu.be/7gSWd2hodFU
import cv2

# get default webcam feed
feed = cv2.VideoCapture(0)
# load target image to detect and map onto (ignore filename)
target = cv2.imread("source.jpg")
# load source video to project onto the target
source = cv2.VideoCapture("cat.mp4")

# get the first frame of the source. If it fails the source will stop being read
read, frame = source.read()

# resizing target and source to be the same
# .shape on a loaded image returns a tuple of height, width, and channels
h, w, c = target.shape
frame = cv2.resize(frame,(w,h))

# read the webcam in a loop
while True:
    webRead, webFrame = feed.read()
    cv2.imshow("webcam",webFrame)
    cv2.imshow("source", frame)
    cv2.imshow("target", target)
    cv2.waitKey(0)
