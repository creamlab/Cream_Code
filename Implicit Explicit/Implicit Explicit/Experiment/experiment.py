# coding=utf-8

# ---------------------------------------------------------------------------- #
# Implicit and explicit identity recognition task using DAVID transformations  #
#                           Laura Rachman - May 2017                           #
#           Generation of stimulus lists randomized for each subject           #
# ---------------------------------------------------------------------------- #

import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
import csv
import codecs
import datetime
import glob
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual,event,core,sound,logging,gui

#-------------------------------------------------------------------

#    Function to get list of relevant files in trial_file folder
#    i.e. not taking into account files that start with '.'

def myListDir(directory):
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]


win = visual.Window([1920,1080],fullscr=False,allowGUI=True,color="lightgray", units='norm')

#    Set paths
DIR = os.path.dirname(os.path.realpath(__file__))
imPath = os.path.join(DIR, 'images/')
soundPath = os.path.join(DIR, 'stimuli/')


####################################
#             Functions            #
####################################


#    Function to read the trialFile that has been made for the subject and returns pairs of audio files for each trial

def getTrials(subjNr, testID, outfile, trialFilePath):
    ppnr = format(subjNr,'02')
    trialFile = open(''.join(glob.glob('trial_lists/id_' + testID + '_s'+ ppnr +'_*.csv')),'rb')
    reader = csv.reader(trialFile, delimiter=',')
    trialList = list(reader)

    outHeaders = trialList[0]
    outHeaders.extend(('response', 'responseCode', 'responseTime'))

    with open(outfile, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = outHeaders)
        writer.writeheader()

    trialList = trialList[1::]
    stimList = []

    for line in trialList:
        stimulus = [line[0],line[1]]
        stimList.append(stimulus)

    return stimList,trialList

#    Function to show texts for instructions
#    between blocks
#    and at the end of the experiment

def showText(fileName):
    with codecs.open (fileName, "r", "utf-8") as file :
        message = file.read()

    startExp = visual.TextStim(win, text = message, color = 'black')
    startExp.height = 0.05
    startExp.draw()
    win.flip()

    while True :
        if len(event.getKeys()) > 0 : break
        event.clearEvents()
        core.wait(0.2)


#    Function to draw all objects at once
def drawStartTrial():
    attention.draw()
    core.wait(0.5)
    attention.setColor('black')
    attention.draw()

def drawResponse():
    old.draw()
    new.draw()
    oldBox.draw()
    newBox.draw()

def drawObjects(testID):
    if testID == 'implicit':
        instruction1.draw()
    elif testID == 'explicit':
        instruction2.draw()
    for item in drawList: item.draw()
    for label in labelStim: label.draw()
    for box in checkBox: box.draw()
    for square in squareList: square.draw()


####################################
#            Play sounds           #
####################################

labelSize = 0.07

label1 = visual.TextStim(win, units='norm', text='A', color='black', height=3*labelSize, pos=(0,0))
label2 = visual.TextStim(win, units='norm', text='B', color='black', height=3*labelSize, pos=(0,0))

instruction1 = visual.TextStim(win, units='norm', text='Les deux mots, sont-ils produits par le m'+u'\u00EA'.encode('utf-8')+'me locuteur?', color='black', height=labelSize, pos=(0,0.1), alignHoriz='center')
instruction2 = visual.TextStim(win, units='norm', text='Avez-vous entendu votre propre voix ?', color='black', height=labelSize, pos=(0,0.1), alignHoriz='center')

square1 = visual.ShapeStim(win
                            , fillColor = None
                            , lineColor = None
                            , opacity = 1
                            , units = 'norm'
                            , vertices=[ (-0.6, 0.5-3*labelSize)
                                       , (-0.6, 0.5-1*labelSize)
                                       , (-0.4, 0.5-1*labelSize)
                                       , (-0.4, 0.5-3*labelSize)
                                        ]
                            )
                     
square2 = visual.ShapeStim(win
                            , fillColor = None
                            , lineColor = None
                            , opacity = 1
                            , units = 'norm'
                            , vertices=[ (0.4, 0.5-3*labelSize)
                                       , (0.4, 0.5-1*labelSize)
                                       , (0.6, 0.5-1*labelSize)
                                       , (0.6, 0.5-3*labelSize)
                                        ]
                            )

attention = visual.TextStim(win, units='norm', text='+', color='gray', height=3*labelSize, pos=(0,0), alignHoriz='center')


fixation = visual.TextStim(win, units='norm', text='+', color='black', height=1.5*labelSize, pos=(0,0.1), alignHoriz='center')

####################################
#           Rating scale           #
####################################

xPos = -0.1
yPos = -0.2
labels = ['oui','non']
labelColor = 'black'
labelSize = 0.07
drawList = []

#    Ratio for image scaling
screenRatio = (float(win.size[1])/float(win.size[0]))

#    Space between labels
labelSpace = abs(-0.8 - yPos)/(len(labels)+1)

#    List for response options
labelStim = []
checkBox = []
squareList = []
for index in range(len(labels)):
    y = yPos - labelSpace * index
    labelStim.append(visual.TextStim(win, units = 'norm', text = labels[index], alignHoriz='left', height=labelSize, color=labelColor, pos=(xPos,y)))
    checkSize = labelSize
    checkBox.append(visual.ImageStim(win, image=imPath+'rb_off.png', size=(checkSize*screenRatio,checkSize), units='norm', pos=(xPos-checkSize, y-labelSize*.05)))
    squareList.append(visual.ShapeStim(win
                            , fillColor = None
                            , lineColor = None
                            , opacity = 1
                            , units = 'norm'
                            , vertices=[(xPos-1.3*checkSize, y-labelSize*.3)
                                       , (xPos-1.3*checkSize, y+labelSize*.3)
                                       , (xPos-0.7*checkSize, y+labelSize*.3)
                                       , (xPos-0.7*checkSize, y-labelSize*.3)
                                        ]
                            )
                     )

####################################
#         Start experiment         #
####################################

def trialLoop():

#    Query participants informations    
    subjectInfo = {'Number':100, u'Test ID': u'implicit/explicit'}
    dlg = gui.DlgFromDict(subjectInfo, title=u'phrases')
    if dlg.OK:
        subjNr = subjectInfo['Number']
        testID = subjectInfo['Test ID']
        
    else:
        core.quit()       #   The user hit cancel so exit

    
    ppnr = format(subjNr, '02')

#    Save a log file for detail verbose info
    filename = 'subj'+ ppnr
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)                      #    This outputs to the screen, not a file

    mouse = event.Mouse()
    date = datetime.datetime.now()
    
    resultsFile = os.path.join(DIR,'results/id_' + testID + '_subj'+format(subjNr,'02')+'_'+date.strftime('%y%m%d_%H.%M')+'.csv' )
    print resultsFile

    trialFilePath = os.path.dirname(__file__)+'/trial_lists/'

    stimList, trialList = getTrials(subjNr, testID, resultsFile, trialFilePath)

#    Start trials
    totalTrials = len(stimList)    #    Number of trials in the list
    counter = 0

    time = core.Clock()
    core.wait(1)

    showText(fileName = "intro_"+ testID +".txt")   #   Instructions
    showText(fileName = "practice.txt")             #   Announcement of practice trials

#################
# Practice trials
#################

    practiceList = [['s01_w03_neutral.wav', 's01_w11_neutral.wav'], ['s03_w05_neutral.wav', 's03_w06_neutral.wav']]
    for fileName in practiceList :
        stim_ref = sound.Sound(value=soundPath+fileName[0])
        stim = sound.Sound(value=soundPath+fileName[1])
        endTrial = False
        selected = None
        drawStartTrial()
        win.flip()
        core.wait(1)
        label1.draw()
        win.flip()
        core.wait(.3)
        label1.draw()
        stim_ref.play()
        core.wait(1.8)
        win.flip()
        win.flip()
        core.wait(.8)
        label2.draw()
        win.flip()
        core.wait(.3)
        label2.draw()
        stim.play()
        core.wait(1.8)

        trialTimer = core.Clock()
        trialTimer.reset()
        startTime = time.getTime()

        while (not endTrial):
            drawObjects(testID)
            win.flip()
            while mouse.getPressed()[0] == 0:
                drawObjects(testID)
                win.flip()

            #    Loop for multiple choice response    
            for index in range(len(checkBox)):
                if mouse.isPressedIn(squareList[index]):
                    selected = index
        
                    while mouse.getPressed()[0] == 1:
                        drawObjects(testID)
                        win.flip()              

                    endTime = time.getTime()
                    rt = endTime - startTime
                    rt = round(rt, 2)
                    response = selected
                    print response, rt
                    endTrial = True
                    win.flip()
                    core.wait(0.5)                   #    Blank screen before the start of the next trial
            while mouse.getPressed()[0] == 1:
                drawObjects(testID)
                win.flip()
                core.wait(1.3)                       #    1.3 s after the play button is clicked, the letters will turn black again
                label1.setColor('black')
                label2.setColor('black')


    showText(fileName = "endpractice.txt")

#############################################
# Experimental trials
# 4 blocks of 36 trials = 144 trials in total
#############################################

    nblocks = 4
    ntrials = len(stimList)/nblocks 
    for iblock in range(nblocks):
        
        #    Loop per trial
        for fileName in stimList[(0)+ntrials*iblock:(ntrials)+ntrials*iblock] :
            stim_ref = sound.Sound(value=soundPath+fileName[0])
            stim = sound.Sound(value=soundPath+fileName[1])
            endTrial = False
            selected = None
            drawStartTrial()
            win.flip()
            core.wait(1)
            label1.draw()
            win.flip()
            core.wait(.3)
            label1.draw()
            stim_ref.play()
            core.wait(1.8)
            win.flip()
            win.flip()
            core.wait(.8)
            label2.draw()
            win.flip()
            core.wait(.3)
            label2.draw()
            stim.play()
            core.wait(1.8)
    
            trialTimer = core.Clock()
            trialTimer.reset()
            startTime = time.getTime()
    
            while (not endTrial):
                drawObjects(testID)
                win.flip()
                while mouse.getPressed()[0] == 0:
                    drawObjects(testID)
                    win.flip()
    
                #    Loop for multiple choice response    
                for index in range(len(checkBox)):
                    if mouse.isPressedIn(squareList[index]):
                        selected = index
            
                        while mouse.getPressed()[0] == 1:
                            drawObjects(testID)
                            win.flip()              
    
                        endTime = time.getTime()
                        rt = endTime - startTime
                        rt = round(rt, 2)
                        response = selected
                        print response, rt
                        endTrial = True
                        win.flip()
                        core.wait(0.5)                   #    Blank screen before the start of the next trial
                while mouse.getPressed()[0] == 1:
                    drawObjects(testID)
                    win.flip()
                    core.wait(1.3)                       #    1.3 s after the play button is clicked, the letters will turn black again
                    label1.setColor('black')
                    label2.setColor('black')
    
            #    Write results to file
            if testID == 'implicit':
                if response == 0:
                    responseCode = 'same'
                elif response == 1:
                    responseCode = 'different'
            elif testID == 'explicit':
                if response == 0:
                    responseCode = 'self'
                elif response == 1:
                    responseCode = 'other'

    
            trialList[counter].extend((response, responseCode, rt))
            with open(resultsFile, 'a') as fout :
                writer = csv.writer(fout)
                writer.writerow(trialList[counter])
    
            counter += 1                             #    Trial counter adds 1 before starting the next trial

        if iblock<(nblocks-1):                       #    -> End of block
            showText(fileName = "pause.txt")
        else:                                        #    else -> End of experiment
            if testID is 'implicit':
                showText(fileName = "outro.txt")
            elif testID is 'explicit':
                showText(fileName = "outro_end.txt")


    # Close Python
    win.close()
    core.quit()

    time.sleep(2)
    sys.exit()





#   Running the file as a script (instead of importing it) creates a sample file
if __name__ == "__main__":
    trialLoop() 

