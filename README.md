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
![IKEA Place example image](/assets/ikea.webp)
Ikea Place is an app provided by the Swedish furniture company. It allows users who are browsing for furniture
to place it inside of their home using their smartphone's camera. Allowing them to compare the size and aesthetic
of the items. It also enourages users to create a more personal connection with the item being placed into their home
via AR; making the app an effective sales technique. This relates to my project as it uses a projection in AR
through a phone camera/webcam. It adjusts based on the movement of the camera. However my project does differ
in some ways. Firstly, I would also have to adjust for when the camera is steady but the target (magazine) is moving. 
In IKEA Place, it's unlikely the target (floor or desk) would move instead of the camera. I also am using a different
source. My AR is using a video feed whereas this uses a 3D model. The applications of my product are also different,
being made for art and entertainment rather than commercial sales. 

#### Example 2: Snapchat filters
![Snapchat filter example image](/assets/snap.webp)
Snapchat filters are much more different to my project than Ikea Place. These AR filters track a users face to project
things like masks, beards, tatoos and more onto them. It can be both 2D or 3D projections and they can respond to the 
users (for example some have physics implementations like to make wobbly noses when a persons head moves). I think the 
purpose of this product is more towards entertainment than Ikea Place, but much more so than my project. Snapchat filters
are purely entertainment and novelty whereas AR magazine covers would be also informational. And of course theres the
obvious difference in mine being non-3D model based.

#### Example 3: Pokemon GO
![Pokemon GO example inage](/assets/poke.webp)
Pokemon Go is a 2016 mobile app which uses the iconic characters from Pokemon to make a location based video game.
Users would have to physically move outside and the phone's GPS would register their location and move their character.
Based on this they would encounter 'Pokemon' which they could try to 'capture'; capturing them is where AR and the link
to my project arises as it would use the phones camera to AR project a 3D pokemon model. The user can also drag their
finger across the screen to 'throw' a ball to catch them. My project doesn't involve this level of interactivity with
the AR projection which could be something I need to consider implementing. 

## Documented Design:
![Keypoint markers drawn using OpenCV](/assets/keypoints.png)
Above is an example of how OpenCV and it's ORB methods can be used to create a series of keypoints.
These unique keypoints can uniquely indentify a target image. It even works through a webcam with non-ideal alignment or lighting
thanks to being able to allow a certain degree of inaccuracy to still be accepted as a match. In the image above, OpenCV draws the matching points 
to demonstrate which areas correlate to the same points on the source. This will be important for my project as I need to recognize several magazine
covers apart and load specific source videos to overlay on top. The source code for this can be found in keypointDetection.py.

![Border detection with homography and OpenCV](/assets/border.png)
Here I add onto the above python file by taking the keypoints and relating them to the same keypoints found through the webcam.
The difference in their distances allows for a homography matrix to be calculated. To do this I created a numpy array of the successful
keypoints and used .reshape() to format it as a 2D array of 2 keypoints each. This is the accepted format for matching homography using cv2. 
This numpy array has to also be made for the keypoints in the original image. From this calculation we get a homography matrix.
If done successfully this gives the data to perform a warp which matches to the image in the webcam. I then use cv2.perspectiveTransform to 
apply this warp to the border coordinates of the target image. This is then projected onto the webcam frame and can be seen above as the white
box. 

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
