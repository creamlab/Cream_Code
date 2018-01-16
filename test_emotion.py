# coding=utf-8

import time
import sys
import os
import csv
import codecs
import datetime
import randomiseFiles
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import visual,event,core,sound

#-------------------------------------------------------------------
# Function to get list of relevant files in trial_file folder
# i.e. not taking into account files that start with '.'
def myListDir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]

#-------------------------------------------------------------------

# Experiment parameters
testLanguage = 'French'
testID = 'emotion'
date = datetime.datetime.now()

trialFilePath = os.path.dirname(__file__)+'/trial_files/emotion/'
trialFileList = myListDir(trialFilePath)
subjNr = len(trialFileList)+1
# If the experiment is interrupted before the end comment out lines 32 and 38 by putting the symbol '#' at the beginning of the line.
# The uncomment line 35 by removing the '#' and fill in the correct subject number
#subjNr = 
 
# Generates a new file in trial_files folder with order of trials
randomiseFiles.main(subjNr,subjNr,testID,testLanguage)


# Set directory paths
imPath = os.path.dirname(__file__)+'/images/'
soundPath = os.path.dirname(__file__)+'/sounds/'
resultsFile = os.path.dirname(__file__)+'/results/emotion/subj'+str(subjNr)+'_'+testLanguage+'_'+date.strftime('%y%m%d_%H.%M')+'.csv'        # writes a new csv file in which to save the experiment results


# Screen / mouse parameters
win = visual.Window([1440,900],fullscr=True,color="lightgray", units='norm')
mouse = event.Mouse()

# Ratio for image scaling
screenRatio = (float(win.size[1])/float(win.size[0]))
print screenRatio



####################
#-----Functions-----
####################


# reads the trialFile that has been made for the subject and returns pairs of audio files for each trial
def getTrials(subjNr = None, outfile = resultsFile, trialFilePath = trialFilePath, lang = testLanguage):

    trialFile = trialFilePath+lang+'_trialList_subj'+str(subjNr)+'.csv'     # reads csv file with order of trials for each subject
    
    with open(trialFile, 'rb') as ftrials :
        reader = csv.reader(ftrials)
        trialList = list(reader)

    outList = []
    outHeaders = trialList[0]
    outHeaders.extend(('file_s1', 'file_s2', 'responseCode', 'response', 'responseTime', 'timesPlayed_s1', 'timesPlayed_s2'))

    with open(outfile, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = outHeaders)
        writer.writeheader()

    trialList = trialList[1::]
    stimList = []

    for line in trialList:
        audioPair = [ str(line[0]) + str(line[1]) + str(line[2]) + str(line[3]) + '_ref.wav',
                      str(line[0]) + str(line[1]) + str(line[2]) + str(line[3]) + str(line[4]) + '.wav' ]
        stimList.append(audioPair)


    return stimList,trialList

# function to show texts for instructions, between blocks, and at the end of the experiment
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


# function to draw all objects at once
def drawObjects():
    play1.draw()
    play2.draw()
    label1.draw()
    label2.draw()
    square1.draw()
    square2.draw()
    instruction.draw()
    for item in drawList: item.draw()
    for label in labelStim: label.draw()
    for box in checkBox: box.draw()
    for square in squareList: square.draw()
    next.draw()
    nextBox.draw()






######################
#-----play sounds-----
######################

labelSize = 0.07

label1 = visual.TextStim(win, units='norm', text='VOICE 1', color='black', height=0.8*labelSize, pos=(-0.5,0.5))
label2 = visual.TextStim(win, units='norm', text='VOICE 2', color='black', height=0.8*labelSize, pos=(0.5,0.5))
instruction = visual.TextStim(win, units='norm', text='Compared to Voice 1, Voice 2 sounds ...', color='black', height=labelSize, pos=(0,0.1), alignHoriz='center')

play1 = visual.ImageStim(win, image=imPath+'play2.png', units='norm', size = (0.15*screenRatio,0.15), pos=(-0.5,0.5-2*labelSize))
play2 = visual.ImageStim(win, image=imPath+'play2.png', units='norm', size = (0.15*screenRatio,0.15), pos=(0.5,0.5-2*labelSize))

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




#######################
#-----rating scale-----
#######################



xPos = -0.1
yPos = -0.2
labels = ['happy','sad', 'afraid', 'neutral', 'none of the above']
labelColor = 'black'
labelSize = 0.07
drawList = []

# Ratio for image scaling
screenRatio = (float(win.size[1])/float(win.size[0]))

# Space between labels
#labelSpace = abs(-1.9 - yPos)/(len(labels)+1)
labelSpace = abs(-0.8 - yPos)/(len(labels)+1)


# List for response options
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




# Settings for NEXT button
next = visual.ImageStim(win, image = imPath+'next_press.png', units = 'norm', pos=(0,-0.85))

nextBox = visual.ShapeStim(win
                        , fillColor = None
                        , lineColor=  None
                        , units = 'norm'
                        , vertices=[ (-0.2*screenRatio, -1  )
                                   , (-0.2*screenRatio, -0.7) 
                                   , ( 0.2*screenRatio, -0.7) 
                                   , ( 0.2*screenRatio, -1  )
                                   ]
                        )



time = core.Clock()
stimList, trialList = getTrials(subjNr)


###########################
#-----start experiment-----
###########################


showText(fileName = "intro_emotion_FR.txt")     # text with instructions for the experiment
showText(fileName = "practice_FR.txt")             # announcement of practice trials


# start trials


totalTrials = len(stimList) - 4    # number of trials in the list minus four practice trials
counter = 0


# loop per trial
for trialNr in stimList :
    next.setImage(imPath+'next_press.png')
    for index in range(len(checkBox)):
        checkBox[index].setImage(imPath+'rb_off.png')
    s1 = sound.Sound(value=soundPath+trialNr[0])
    s2 = sound.Sound(value=soundPath+trialNr[1])
    timesPlayedS1 = 0
    timesPlayedS2 = 0
    endTrial = False
    selected = None
#    noResponse = False
#    timesClicked = 0
    time = core.Clock()
    startTime = time.getTime() 

    while (not endTrial):
        drawObjects()
        win.flip()
        while mouse.getPressed()[0] == 0:
            drawObjects()
            win.flip()

        # loop for multiple choice response    
        for index in range(len(checkBox)):
            if mouse.isPressedIn(squareList[index]):
                next.setImage(imPath+'next.png')
                if selected == None:
                    selected = index
                    checkBox[index].setImage(imPath+'rb_on.png')
                else: 
                    if selected == index:
                        selected = None
                        checkBox[index].setImage(imPath+'rb_off.png')
                        next.setImage(imPath+'next_press.png')
                    elif selected != index:
                        checkBox[selected].setImage(imPath+'rb_off.png')
                        checkBox[index].setImage(imPath+'rb_on.png')
                        selected = index
                while mouse.getPressed()[0] == 1:
                    drawObjects()
                    win.flip()              

        if mouse.isPressedIn(square1):      # plays voice 1 upon clicking the play button
            label1.setColor('green')
            timesPlayedS1 += 1
            print 'voice 1 played '+str(timesPlayedS1)+' times'
            s1.play()
        elif mouse.isPressedIn(square2):    # plays voice 2 upon clicking the play button
            label2.setColor('green')
            timesPlayedS2 += 1
            print 'voice 2 played '+str(timesPlayedS2)+' times'
            s2.play()    
        elif mouse.isPressedIn(nextBox) and selected != None:        # collects clicks on next button: end of trial
            endTime = time.getTime()
            rt = endTime - startTime
            rt = round(rt, 2)
            response = selected
            print response, rt
            endTrial = True
            win.flip()
            core.wait(0.5)                   # blank screen before the start of the next trial
        while mouse.getPressed()[0] == 1:
            drawObjects()
            win.flip()
            core.wait(1.3)                   # 1.3 s after the play button is clicked, the letters will turn black again
            label1.setColor('black')
            label2.setColor('black')

    # write results to file
    if response == 0:
        responseCode = 'h'
    elif response == 1:
        responseCode = 's'
    elif response == 2:
        responseCode = 'a'
    elif response == 3:
        responseCode = 'n'
    else:
        responseCode = 'x'

    trialList[counter].extend(( trialNr[0], trialNr[1], responseCode, response, rt, timesPlayedS1, timesPlayedS2 ))
    with open(resultsFile, 'a') as fout :
        writer = csv.writer(fout)
        writer.writerow(trialList[counter])

    counter += 1 # trial counter adds 1 before starting the next trial

    if counter == 3:
        showText(fileName = "start_test_FR.txt")

    elif counter == totalTrials/4 + 4 or counter == 2*totalTrials/4 + 4 or counter == 3*totalTrials/4 + 4 :
        showText(fileName = "pause_FR.txt")

# End of experiment

showText(fileName = "outro_FR.txt")

# Close Python

win.close()
core.quit()
sys.exit()







