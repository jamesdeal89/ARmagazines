# Computer Science NEA - AR Video Magazine Covers
### Introduction:
My project idea is to create either an investigation into, or a finalized app
product which overlays a video of a pre-recorded magazine cover where the 
main image model is moving. This video is to be overlain on top of a printed
magazine in real life (Augmented Reality). It should follow and adapt to the movements
and angling that the camera is taking footage from. 

### Analysis:
#### Example 1: IKEA Place
![IKEA Place example image](/assets/ikea.webp)
Ikea Place is an app provided by the Swedish furniture company. It allows users who are browsing for furniture
to place it inside of their home using their smartphone's camera. Allowing them to compare the size and aesthetic
of the items. It also enourages users to create a more personal connection with the item being placed into their home
via AR; making the app an effective sales technique. This relates to my project as it uses a projection in AR
through a phone camera/webcam. It adjusts based on the movement of the camera. However my project does differ
in some ways. Firstly, I would also have to adjust for when the camera is steady but the target (magazine) is moving. 
In IKEA Place, it's unlikely the target (floor or desk) would move instead of the camera. I also am using a different
source. My AR is using a video feed whereas this uses a 3D model. 

#### Example 2: Snapchat filters
![Snapchat filter example image](/assets/snap.webp)

#### Example 3: Pokemon GO
![Pokemon GO example inage](/assets/poke.webp)

### Documented Design:
![Keypoint markers drawn using OpenCV](/assets/keypoints.png)

### Bibliography:

https://docs.opencv.org/3.4/d9/dab/tutorial_homography.html
- OpenCV homography documentation

https://medium.com/acmvit/how-to-project-an-image-in-perspective-view-of-a-background-image-opencv-python-d101bdf966bc
- Perspective warping images onto each other

https://pyimagesearch.com/2021/01/04/opencv-augmented-reality-ar/
- Projecting images onto marker cards

https://youtu.be/oXlwWbU8l2o
- YouTube OpenCV Course

https://youtu.be/7gSWd2hodFU
- YouTube OpenCV video series; specifically on Augmented Reality

https://learnopencv.com/image-alignment-feature-based-using-opencv-c-python/
- OpenCV ORB image alignment
