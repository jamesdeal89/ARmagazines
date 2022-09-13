# reading video
import cv2

# video can be read using cv2.VideoCapture
# this is done in individual video frames being processed
# a webcam feed can be used by passing in 0 for the default webcam 
# a saved video file uses a string of the filepath
capture = cv2.VideoCapture('cat.mp4')

# using a loop we can iterate through frames
while True:
    # get next frame
    isTrue, frame = capture.read()
    # resize next frame 
    frame = cv2.resize(frame,(600,400))
    # display the frame
    cv2.imshow(winname='video',mat=frame)
    # wait for any keypress and stop if it's letter q
    key = cv2.waitKey(1)
    if key == 81:
        break
# stops loading video
capture.release()
cv2.destroyAllWindows()


