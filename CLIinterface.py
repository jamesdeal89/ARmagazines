"""
For this iteration I want to add a comand line interface to make loading target magazine covers and source
videos more user friendly. I want to progress this further by using PySimpleGUI to make a full GUI.
Additionally I think it's important to allow for more than 3 targets/sources and that will require using
file I/O to store and loops to iterate through the saved locations and make variables for each.
Further functionalisation of my code may be required to make using infinitely more targets possible.
"""
import PySimpleGUI as sg
import sys
import cv2
import numpy as np
import csv
import re
import os

def recognizeCover():
    ...

def webcamRead(feed, targets, sources, orb, orbList):
    # load the webcam frame
    frameLoaded, webFrame = feed.read()
    loadedSources = []
    loadedSourceFramePairs = []
    # load the frame of every source video
    for source in sources:
        loaded, sourceFrame = sources[source].read()
        loadedSourceFramePairs.append(loaded, sourceFrame)
        loadedSources.append(loadedSourceFramePairs)
    while frameLoaded:
        # find the keypoints and descriptors in the webframe
        keyPointsWeb, descriptorsWeb = orb.detectAndCompute(webFrame,None)
        matches, targetNum = recognizeCover()

def createORB(targets):
    orb = cv2.ORB_create(nfeatures=1000)
    orbList = {}
    counter = 0
    for target in targets:
        # using cv2 ORB which is a feature which creates image detector keypoints
        # nfeatures specifices the number of features to use as matching points
        # positioning relationships and arrangements of pixels are used
        keyPoints, descriptors = orb.detectAndCompute(target,None)
        KPandDESCpair = []
        KPandDESCpair.append(keyPoints, descriptors)
        orbList["pair"+ str(counter)] = KPandDESCpair
        counter += 1
    return orb, orbList

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
    generateCSV(targetSource,createOrUpdate)
     


def loadPairs():
    # use a csv file to load the target and source pairs using loops
    # after this the loaded pairs will be passed into a function which uses OpenCV and iterative loops
    # to load all the pairs into OpenCV image objects.
    with open("pairs.csv") as file:
        reader = csv.reader(file)
        targets = {}
        sources = {}
        counter = 0
        for row in reader:
            targets["target"+ str(counter)] = cv2.imread(row["target"])
            sources["source"+ str(counter)] = cv2.VideoCapture(row["source"])
            counter += 1
        return targets, sources


def main():
    while True:
        loadOrGen = GUI()
        #loadOrGen = input("Do you want to load, generate, or update a target-source pair file? (L,G, or U)").strip().lower()
        if loadOrGen == "l":
            try:
                # get the tuple of loaded target cv2 objects and loaded source cv2 objects
                targets, sources = loadPairs()
            except FileNotFoundError:
                # catch any error where the file pairs.csv does not exist and exit while giving error message
                sys.exit("Tshere was no pairs.csv file found in the local directory. File must be named pairs.csv to load.")
            else:
                # if the pair loading was successful we can break the loop for checking input
                break
        elif loadOrGen == "g":
            # call the generate function and pass in "w" to create or overwrite a pairs.csv file
            generatePairs("w")
            break
        elif loadOrGen == "u":
            # using the same generate function except pass in "a" to append to an already exisiting pairs.csv file
            generatePairs("a")
            break
    # get a dictionary of every target's keypoints and descriptors. 
    orb, orbList = createORB(targets)
    # load the webcam
    feed = cv2.VideoCapture(0)
    webcamRead(feed, targets, sources, orb, orbList)



if __name__ == "__main__":
    main()