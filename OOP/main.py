"""In this file I want to create a class structure for my code. This is based upon the projectvideo.py file.
My plan is to create a 'file' class which then allows for a source, target and webcam class to inherit from. 
Then a main() function will create instances of these classes and run the iteration and processesing for some aspects.
I want to make processing inside class methods as much as I can so I'm going to make the warping of images, projection and 
detection into their own objects.  
Some classes will be placed in a filesystem of objects which are in this folder.
Overall this file will be focused on GUI implementation and calling class methods."""

# import our external libraries of:
# OpenCV for image manipulation, 
# PySimpleGUI for GUI, 
# os is for identify filepaths,
# sys is for error handling,
# and built-in python csv library for saving and loading data
import cv2
import PySimpleGUI as sg
import csv
import os
import sys
from warp import Warp
from project import Project
from detect import Detect
from border import Border
from webcam import Webcam
from source import Source
from target import Target
from search import Search

def GUIgen():
    """The second GUI to get the target and source file locations"""
    event, values = sg.Window('Provide the files', [[sg.Text("This will pop-up continously until 'finish' button is pressed")],[sg.Text('File for target magazine cover')], [sg.Input(), sg.FileBrowse()],[sg.Text('File for source video to be projected')], [sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Button('Finish')] ]).read(close=True)
    if event == 'Finish':
        return None, None
    else:
        return values[0], values[1]

def GUI():
    """This is the first GUI page which gets the user to either provide or generate a .csv pair file"""
    # set the theme
    sg.theme('DarkAmber') 
    # sets the layout of the GUI
    layout = [  [sg.Text('For the AR to work, a savefile of source videos and target magazine cover images needs to be loaded.')],
                [sg.Text('How to continue?:')],
                [sg.Button('Load'), sg.Button('Generate'), sg.Button("Update") ]  ]
    # makes a window
    window = sg.Window('AR Magazine Projector', layout)
    # loops to scan for events and capture user inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: 
            break
        elif event == 'Load':
            return "l"
        elif event == 'Generate':
            return "g"
        elif event == 'Update':
            return "u"
    # close the window if the user breaks the event check loop
    window.close()

def generateCSV(pairings, createOrUpdate):
    # this will use file I/O and the csv library to take the pairing dictionary list and either write or append to 
    # a pairs.csv file.
    with open("pairs.csv",createOrUpdate) as file:
        # use the csv library's dictionary writer to make the .csv file's heading (if creating) and for later writing each dict
        dictwriter = csv.DictWriter(file, fieldnames=pairings[0].keys())
        if createOrUpdate == "w":
            dictwriter.writeheader()
        # iterate through the pairs list to get each dictionary 
        for pair in pairings:
            dictwriter.writerow(pair)
        return loadPairs()

def generatePairs(createOrUpdate):
    # create a csv file of the target and source pairs if one does not exist
    # allow user to keep entering target and source pair filenames with .mp4 and .jpeg images until ctrl+D
    # verify input using regex
    targetSource = []
    while True:
        pairing = {}
        fileTarget, fileSource = GUIgen()
        if fileTarget == None:
            break
        # seperate the file extensions using os library 
        name,ext = os.path.splitext(fileTarget)
        name1,ext1 = os.path.splitext(fileSource)
        # check that both file extensions are valid to avoid OpenCV compatability errors
        if ext in [".jpg",".jpeg"] and ext1 == ".mp4":
            # if valid update the dictionary pair and append it to the list
            pairing["target"] = fileTarget
            pairing["source"] = fileSource
            targetSource.append(pairing)
        else:
            sg.popup('ERROR', 'File extension must be .jpeg/.jpg for the target and .mp4 for the source')
    # once loop is broken we call the file generator function
    return generateCSV(targetSource,createOrUpdate)

def loadPairs():
    with open("pairs.csv", "r") as file:
        reader = csv.DictReader(file)
        targets = []
        sources = []
        counter = 0
        for row in reader:
            # we make an append to an array of each object we create for target and source respectively
            targets.append(Target(row["target"],sourceObj=Source([row["source"]])))
            counter += 1
        return targets

def main():
    # TODO: Create a 'performance' mode the user can select in GUI -> only load or check for first detected source/target
    # TODO: Create own image recognition class <- almost done
    while True:
        loadOrGen = GUI()
        #loadOrGen = input("Do you want to load, generate, or update a target-source pair file? (L,G, or U)").strip().lower()
        if loadOrGen == "l":
            # create an instance of the search class ass set the target as the pairs file and the files to search as the current working directory
            path = os.getcwd()
            search = Search("pairs.csv", os.listdir(path))
            search.sort()
            if search.search():
                # get the tuple of loaded target cv2 objects and loaded source cv2 objects
                targets = loadPairs()
                break
            else:
                sys.exit("ERROR - pairs.csv file not found. please generate first.")
        elif loadOrGen == "g":
            # call the generate function and pass in "w" to create or overwrite a pairs.csv file
            targets = generatePairs("w")
            break
        elif loadOrGen == "u":
            # using the same generate function except pass in "a" to append to an already exisiting pairs.csv file
            targets = generatePairs("a")
            break
    # now that we have the data for every target and source intialized in a dictionary we can begin using the class methods to create the ouput
    # first we intialize the webcam
    webcam = Webcam()
    webcam.load()
    targets[0].load()
    targets[0].getSourceObj().load()
    # resize to be 0.7x size to increase framerate
    targets[0].resize(int(targets[0].getLoadedObj().shape[1]*0.7),int(targets[0].getLoadedObj().shape[0]*0.7))
    h1,w1,c1 = targets[0].getLoadedObj().shape
    targets[0].myGenPoints()
    targets[0].genPoints()
    for target in targets[1:]:
        target.getSourceObj().load()
        target.load()
        target.resize(w1,h1)
        # this generates the samples for target detection. This has recently be changed to be outside the loop to increase framerate
        target.myGenPoints()
        target.genPoints()
        # use the Detect class decect() method to get which object is in the frame (if any)
    # now we can create a loop based on each frame of the webcam we load
    while True:
        # call the method which loads the next frame
        result = None
        webcam.next()
        try:
            # NOTE: source objects are stored WITHIN their respective target objects
            for target in targets:
                target.getSourceObj().next(w1,h1)
        except cv2.error:
            # if we fail to load the next frame we should loop the source videos by reloading them now
            targets[0].getSourceObj().load()
            targets[0].getSourceObj().next(w1,h1)
            for target in targets[1:]:
                target.getSourceObj().load()
                target.getSourceObj().next(w1,h1)
        else:
            # use the Detect class detect() method to get which object is in the frame (if any)
            detect = Detect(webcam, targets)
            # this uses a lower level implementation which gets just which target is in the webcam
            detectedTarget = detect.myDetect()
            # this uses a higher level OpenCV implementation which also gets matches for a homography calculation
            result = detect.detect()
            try:
                successfullMatches,detectedTargetCheck = result
            except:
                successfullMatches = None
                detectedTargetCheck = None
        # if there is a targetted magazine detected
        if successfullMatches is not None and detectedTarget is not None:
            border = Border(detectedTarget, webcam, successfullMatches)
            destinationPoints, homographyMatrix = border.border()
            print("BORDER CALCULATED")
            h,w,c = webcam.getFrame().shape
            warp = Warp(target.getSourceObj().getFrame(), homographyMatrix, [w,h])
            warpedSource = warp.warp()
            print("SOURCE WARPED")
            project = Project(webcam.getFrame(), warpedSource, destinationPoints)
            project.project()
            print("PROJECTED ONTO WEBCAM")
            buttonPress = cv2.waitKey(1)
            if buttonPress == 81 or buttonPress == 113:
                sys.exit()
        else:
            # if there is no detected target, we still display the plain webcam to keep motion smooth
            cv2.imshow("Output",webcam.getFrame())
            buttonPress = cv2.waitKey(1)
            if buttonPress == 81 or buttonPress == 113:
                sys.exit()


# if we're running the main.py file, run the main() subroutine
# this prevents issues with imported files
if __name__ == "__main__":
    main()
