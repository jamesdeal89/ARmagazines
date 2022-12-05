"""In this file I want to create a class structure for my code. This is based upon the projectvideo.py file.
My plan is to create a 'file' class which then allows for a source, target and webcam class to inherit from. 
Then a main() function will create instances of these classes and run the iteration and processesing for some aspects.
I want to make processing inside class methods as much as I can so I'm going to make the warping of images, projection and 
detection into their own objects.  
Some classes will be placed in a filesystem of objects which are in this folder.
Overall this file will be focused on GUI implementation and calling class methods."""

import cv2
import PySimpleGUI as sg

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
    with open("pairs.csv") as file:
        reader = csv.reader(file)
        targets = {}
        sources = {}
        counter = 0
        for row in reader:
            targets["target"+str(counter)] = cv2.imread(row["target"])
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

# if we're running the main.py file, run the main() subroutine
# this prevents issues with imported files
if __name__ == "__main__":
    main()
