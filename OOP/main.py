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
import copy
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
    event, values = sg.Window('Provide the files', [[sg.Text("This will pop-up continously until 'finish' button is pressed")],
                                                    [sg.Text('File for target magazine cover')], 
                                                    [sg.Input(), sg.FileBrowse()],[sg.Text('File for source video to be projected')], 
                                                    [sg.Input(), sg.FileBrowse()], 
                                                    [sg.OK(), sg.Button('Finish')] ]).read(close=True)
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
                [sg.Text('Enter filename (ending in .csv):')],
                [sg.Input()],
                [sg.Text('How to continue?:')],
                [sg.Button('Load'), sg.Button('Generate'), sg.Button("Update") ],  
                [sg.Checkbox('Enable low-level mode? (slower)', default=False, key='lowLevel')],
                [sg.Checkbox('Auto-generate text? (imperfect)', default=False, key='autoText')],
                [sg.Text('Compression size (lower is smaller):')],
                [sg.Slider(range=(0.7, 1.0), resolution=0.1, orientation='horizontal', key='lowRes', default_value=100)]]
    # makes a window
    window = sg.Window('AR Magazine Projector', layout)
    # loops to scan for events and capture user inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: 
            break
        elif event == 'Load':
            window.close()
            # values["-IN-"] returns the boolean value of the checkbox, True meaning ticked
            return "l",values[0],values["lowLevel"],values["lowRes"],values["autoText"]
        elif event == 'Generate':
            window.close()
            return "g",values[0],values["lowLevel"],values["lowRes"],values["autoText"]
        elif event == 'Update':
            window.close()
            return "u",values[0],values["lowLevel"],values["lowRes"],values["autoText"]
    # close the window if the user breaks the event check loop
    window.close()

def generateCSV(pairings, createOrUpdate,fileName,autoText):
    # this will use file I/O and the csv library to take the pairing dictionary list and either write or append to 
    # a pairs.csv file.
    with open(fileName,createOrUpdate) as file:
        # use the csv library's dictionary writer to make the .csv file's heading (if creating) and for later writing each dict
        dictwriter = csv.DictWriter(file, fieldnames=pairings[0].keys())
        if createOrUpdate == "w":
            dictwriter.writeheader()
        # iterate through the pairs list to get each dictionary 
        for pair in pairings:
            dictwriter.writerow(pair)
    return loadPairs(fileName,autoText)

def generatePairs(createOrUpdate, fileName, autoText):
    # create a csv file of the target and source pairs if one does not exist
    # allow user to keep entering target and source pair filenames with .mp4 and .jpeg images until ctrl+D
    # verify input using regex
    targetSource = []
    userNotDone = True
    pairing = {}
    while True:
        fileTarget, fileSource = GUIgen()
        if fileTarget == None:
            break
        # seperate the file extensions using os library 
        name,ext = os.path.splitext(fileTarget)
        name1,ext1 = os.path.splitext(fileSource)
        # check that both file extensions are valid to avoid OpenCV compatability errors
        if ext in [".jpg",".jpeg"] and ext1 == ".mp4":
            # if valid update the dictionary pair and append it to the list
            pairing["target"] = copy.deepcopy(fileTarget)
            pairing["source"] = copy.deepcopy(fileSource)
            targetSource.append(copy.deepcopy(pairing))
        else:
            sg.popup('ERROR', 'File extension must be .jpeg/.jpg for the target and .mp4 for the source')
    # once loop is broken we call the file generator function
    return generateCSV(targetSource,createOrUpdate,fileName,autoText)

def loadPairs(fileName,autoText):
    with open(fileName, "r") as file:
        reader = csv.DictReader(file)
        targets = []
        for row in reader:
            # we make an append to an array of each object we create for target and source respectively
            targets.append(Target(copy.deepcopy(row["target"]),sourceObj=Source(copy.deepcopy([row["source"]]),autoText)))
        return targets

def main():
    while True:
        # Here loadOrGen tells us whether we load fileName or generate a file called fileName. lowLevel determines if we use a mix of my own implementation and OpenCV (slow) or all OpenCV's (fast)
        loadOrGen, fileName, lowLevel, lowRes, autoText = GUI()
        name, ext = os.path.splitext(fileName)
        correctInput = True
        if ext != ".csv":
            sg.popup('error','File extension must be .csv')
            correctInput = False
        if loadOrGen == "l" and correctInput == True:
            # create an instance of the search class ass set the target as the pairs file and the files to search as the current working directory
            path = os.getcwd()
            search = Search(fileName, os.listdir(path))
            search.sort()
            if search.search():
                # get the tuple of loaded target cv2 objects and loaded source cv2 objects
                targets = loadPairs(fileName,autoText)
                break
            else:
                sg.popup('ERROR', 'File not found')
                sys.exit("ERROR - pairs.csv file not found. please generate first.")
        elif loadOrGen == "g" and correctInput == True:
            # call the generate function and pass in "w" to create or overwrite a pairs.csv file
            targets = generatePairs("w",fileName,autoText)
            break
        elif loadOrGen == "u" and correctInput == True:
            # using the same generate function except pass in "a" to append to an already exisiting pairs.csv file
            targets = generatePairs("a",fileName,autoText)
            break
    # now that we have the data for every target and source intialized in a dictionary we can begin using the class methods to create the ouput
    # first we intialize the webcam
    webcam = Webcam(lowRes=lowRes)
    webcam.load()
    targets[0].load()
    targets[0].getSourceObj().load()
    if lowRes:
        # resize to be 0.8x size to increase framerate
        targets[0].resize(int(targets[0].getLoadedObj().shape[1]*lowRes),int(targets[0].getLoadedObj().shape[0]*lowRes))
    h1,w1,c1 = targets[0].getLoadedObj().shape
    targets[0].myGenPoints()
    targets[0].genPoints()
    targets[0].replicateText()
    for target in targets[1:]:
        target.getSourceObj().load()
        target.load()
        target.resize(w1,h1)
        # this generates the samples for target detection. This has recently be changed to be outside the loop to increase framerate
        target.myGenPoints()
        target.genPoints()
        target.replicateText()
        # use the Detect class detect() method to get which object is in the frame (if any)
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
            if lowLevel:
                detectedTarget = detect.myDetect()
            else:
                detectedTarget = None
            # this uses a higher level OpenCV implementation which also gets matches for a homography calculation
            result = detect.detect()
        # if there is a targetted magazine detected
        if (detectedTarget is not None or lowLevel == False) and (result is not None):
            # ensure both my detect and OpenCV's detect are in agreement
            successfullMatches, detectedTargetCheck, arucoBorders = result
            if detectedTarget == detectedTargetCheck or (lowLevel == False):
                if lowLevel == False:
                    detectedTarget = detectedTargetCheck
                border = Border(detectedTarget, webcam, successfullMatches, arucoBorders)
                borderResult = border.border()
                if borderResult != None:
                    destinationPoints, homographyMatrix = borderResult
                    print("BORDER CALCULATED")
                    h,w,c = webcam.getFrame().shape
                    warp = Warp(detectedTarget.getSourceObj().getFrame(), homographyMatrix, [w,h])
                    warpedSource = warp.warp()
                    print("SOURCE WARPED")
                    project = Project(webcam.getFrame(), warpedSource, destinationPoints)
                    # check which mode the program is in
                    if lowLevel:
                        project.myProject()
                    else:
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
