# Computer Science NEA - AR Video Magazine Covers
## Analysis:
### Introduction:
My project idea is to create either an investigation into, or a finalized app
product which overlays a video of a pre-recorded magazine cover where the 
main image model is moving. This video is to be overlain on top of a printed
magazine in real life (Augmented Reality). It should follow and adapt to the movements
and angling that the camera is taking footage from.

### Who is the product for?
I want to create this product to help the school's Media Studies department, specifically Mr.Robson, create new, innovative
interaction methods for student's GCSE, AS, and A level coursework. The coursework all involve creating either a magazine 
or a 'digipack' which also features a cover similar to a magazine. My product will allow them to deepen user 
imersion with their magazine or digipack while joining reality with digital. 

### Main Objectives:
- Read video feeds from a webcam or smartphone camera
- Load source videos of pre-recorded moving covers 
- Detect and recognize which of the source videos matches to the magazine/digipack shown
- Detect edges and borders of the magazine/digipack
- Frame by frame overlay and adjust the warping of the source to match the one in the video
- Thereby creating an AR effect
- Finally adapt the project for a user friendly interface on laptops or a mobile application

### Already existing AR products:
#### Example 1: IKEA Place
<img src="/assets/ikea.webp" alt="IKEA Place example image" width="500"/>
Ikea Place is an app provided by the Swedish furniture company. It allows users who are browsing for furniture
to place it inside of their home using their smartphone's camera. Allowing them to compare the size and aesthetic
of the items. It also enourages users to create a more personal connection with the item being placed into their home
via AR; making the app an effective sales technique. This relates to my project as it uses a projection in AR
through a phone camera/webcam. It adjusts based on the movement of the camera. However my project does differ
in some ways. Firstly, I would also have to adjust for when the camera is steady but the target (magazine) is moving. 
In IKEA Place, it's unlikely the target (floor or desk) would move instead of the camera. I also am using a different
source. My AR is using a video feed whereas this uses a 3D model. The applications of my product are also different,
being made for art and entertainment rather than commercial sales. 
<hr/>

#### Example 2: Snapchat filters
<img src="/assets/snap.webp" alt="Snapchat filter example image" width="500"/>
Snapchat filters are much more different to my project than Ikea Place. These AR filters track a users face to project
things like masks, beards, tatoos and more onto them. It can be both 2D or 3D projections and they can respond to the 
users (for example some have physics implementations like to make wobbly noses when a persons head moves). I think the 
purpose of this product is more towards entertainment than Ikea Place, but much more so than my project. Snapchat filters
are purely entertainment and novelty whereas AR magazine covers would be also informational. And of course theres the
obvious difference in mine being non-3D model based.
<hr/>

#### Example 3: Pokemon GO
<img src="/assets/poke.webp" alt="Pokemon GO example image" width="500"/>
Pokemon Go is a 2016 mobile app which uses the iconic characters from Pokemon to make a location based video game.
Users would have to physically move outside and the phone's GPS would register their location and move their character.
Based on this they would encounter 'Pokemon' which they could try to 'capture'; capturing them is where AR and the link
to my project arises as it would use the phones camera to AR project a 3D pokemon model. The user can also drag their
finger across the screen to 'throw' a ball to catch them. My project doesn't involve this level of interactivity with
the AR projection which could be something I need to consider implementing. 
<hr/>

#### Example 4: Google Maps Live View
<img src="/assets/liveView.webp" alt="Google Live View example image" width=500>
Google in the past few years have rolled out a new feature in Google Maps on mobile. It's called 'Live View' and is used to 
allow you to see floating directional arrows and prompts for where to go if you're unsure in built-up areas with many alleys and possible
routes. This stays tracked in position no matter where you point the smartphone as shown in the example image above. When first hearing of 
this idea it can feel somewhat gimmicky as holding up your phone in front of your face as a viewfinder for naviagtion could be distracting. 
However Google has developed the feature to use Google Street View data, another project where 360 cameras document city streets into a global
database. Therefore when you use the AR Live View feature it not only creates these projections based on GPS, but also calibrates your location
based on the camera feed data; making it useful even as purely a calibration tool. This is especially useful in built-up urban areas with poor
signal.

### Research On Algorithms / Aproaches That Could Be Used:
#### OpenCV Documentation - Displaying Video And Capturing Camera Feeds:
Source: https://docs.opencv.org/4.x/dd/de7/group__videoio.html

This page holds detailed information on how the Open Computer Vision Python library can used to load and write video information.
It states that the syntax for the VideoCapture() method is:

~~~
cv::VideoCapture::VideoCapture(int -> index, int -> apiPreference = CAP_ANY)
~~~

In laymans terms this notation means that this is a part of the CV library which has a VideoCapture method. This can take two parameters:
The index which is an integer and your 'api preference' which is also an integer. The documentation page further elaborates to say that passing in 
a value of '0' will capture from to the systems default video device; typically the webcam. 
#### OpenCV Documentation - Homography Algorithms:
Source: https://docs.opencv.org/3.4/d9/dab/tutorial_homography.html
#### OpenCV Documentation - Bitwise Operators:
Source: https://docs.opencv.org/4.x/d0/d86/tutorial_py_image_arithmetics.html

## Documented Design:
### Prototype Proof-Of-Concept:
<img src="/assets/keypoints.png" alt="Keypoint markers drawn using OpenCV" width="500"/>
Above is an example of how OpenCV and it's ORB methods can be used to create a series of keypoints.
These keypoints can uniquely indentify a target image. It even works through a webcam with non-ideal alignment or lighting
thanks to being able to allow a certain degree of inaccuracy to still be accepted as a match. In the image above, OpenCV draws the matching points 
to demonstrate which areas correlate to the same points on the source. This will be important for my project as I need to recognize several magazine
covers apart and load specific source videos to overlay on top. The way this works is by taking features of the magazine cover and making that a keypoint from the relationship between groups of pixels. For example you can see the bottom of the letters in MUSK are being used to identify the image from how the white pixels are spaced. The source code for this can be found in keypointDetection.py. 
<hr/>
<img src="/assets/border.png" alt="Border detection with homography in OpenCV" width="500"/>
Here I add onto the above python file by taking the keypoints and relating them to the same keypoints found through the webcam.
The difference in their distances allows for a homography matrix to be calculated. To do this I created a numpy array of the successful
keypoints and used .reshape() to format it as a 2D array of 2 keypoints each. This is the accepted format for matching homography using cv2. 
This numpy array has to also be made for the keypoints in the original image. From this calculation we get a homography matrix.
If done successfully this gives the data to perform a warp which matches to the image in the webcam. I then use cv2.perspectiveTransform to 
apply this warp to the border coordinates of the target image. This is then projected onto the webcam frame and can be seen above as the white
box. 
<hr/>
<img src="/assets/mask1.png" alt="White mask frame with a black box where the target is" width="500"/>
Above you can see a mask which is a white frame in the exact same size as the webcam frame. This is actually generated using numpy.zeros() which just makes a matrix of zeros in the resolution we pass in. OpenCV can interpret this matrix as an 'image' and display it for documentation and also for processing. Using the border points we previously created using homography, we can use OpenCV to draw a filled area where the target is in white (255,255,255). Following this we use a bitwise NOT to flip the colours to the target area being black (0,0,0) and the rest of the frame white (255,255,255). Leaving us with the final mask to overlay later. These binary RGB values should be noted as they're essential to the overlaying process. 
<hr/>
<img src="/assets/warpedSource.png" alt="Warped source frame" width="500"/>
Parallel to the mask we also generate this warped perspective of the source frame. This is done using cv2.warpPerspective which warps the frame by the homography matrix generated previously and then takes a width and height tuple. This tuple will allow us to place the warped source frame in the correct position in a 'frame' which is the same size as the webcam frame by passing in the same w and h values.
<hr/>
<img src="/assets/maskAfterANDWithWebcam.png" alt="Mask after bitwise AND with webcam frame" width="500"/>
Using the mask we created two images previously, we load the mask and the webcam frame using OpenCV. OpenCV has a method called bitwise_AND and also similar bitwise operations for all logic operations. Using this AND operation between the two images means that any data which is a 1 in the frst image and also a 1 in the second image will be output as also a 1. However if either of the inputs are 0, 0 will be output. If we link this specifically to the mask we created, the pixel areas where the magazine was not detected were filled with white which in rgb bits is (11111111,11111111,11111111). However where the target magazine was detected we filled with black which is (00000000,00000000,00000000). In contrast the webcam's bits will not be as uniform as white and black pixels and will likely be something similar to (1111000,1010001,1000011) as taken from a random sample pixel. If we apply the logic from the AND operation to the two zones we can understand why the image above is output. Firstly for the non-target areas in the mask, which are white, we will compare to the random sample pixel. If we AND (11111111,11111111,11111111) and (1111000,1010001,1000011) the output will be (1111000,1010001,1000011). As whenever there's a 0 in the webcam bits, there will be a 0 in the output, whenever theres a 1, there will be a 1 in the output. Therefore we can simplify this expression of (WebcamPixel AND WhitePixel) to simply (WebcamPixel). On the other hand, for the targeted zone which is in black, meaning 0 bits, when we do (00000000,00000000,00000000) AND (1111000,1010001,1000011) it will output (00000000,00000000,00000000) which means no matter what the webcam bit was, it will be output as 0. Therefore the logic expression of (WebcamPixel AND BlackPixel) can be simplified to (BlackPixel). Thereby this bit masking process leads to the image you see above which has the the webcam area without the magazine the exact same, but the area with the magazine target masked out in black. 
<hr/>
<img src="/assets/overlaySuccessAfterORbetweenWarpedSourceMaskedWebcam.png" alt="Successful tracked overlay after using bitwise OR between warped source and the masked webcam frame" width="500"/>
Finally we have to compute one more bitwise operation between the previous step's masked webcam frame and the warped source frame. 

### Graphical Interface
For my program, I need to create a user-friendly interface. This is as my client is the schools media studies department who might not have time or the knowledge to hard-code filepaths or to navigate a command-line. Therefore from my research I've found that PySimpleGUI is an effective library to use for this purpose. It allows me to create graphical windows and input boxes which are essential. However, as the name suggests, it keeps the code required to get it working at a minimum. Therefore allowing me to focus on the backend further while still having an effective user interface.

## Bibliography:

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

https://pythonprogramming.net/image-recognition-python/
- Article discussing image recognition algorithms without OpenCV

https://docs.python.org/3/library/tkinter.html
- Documentation on Tkinter for GUI

https://www.pocket-lint.com/apps/news/google/147956-what-is-google-maps-ar-navigation-and-how-do-you-use-it
- Article on Google Live View, used in research for AR similar products
