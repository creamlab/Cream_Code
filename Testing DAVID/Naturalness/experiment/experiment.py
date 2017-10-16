# coding=utf-8

#------------------------------------------------------#
#      Testing the naturalness of modified voices      #
#                 Laura Rachman _ 2015                 #
#------------------------------------------------------#

import time
import sys
import os
import csv
import codecs
import datetime
import randomiseFiles
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual,event,core,sound

#---------------------------------------------------------------
#    Function to get list of relevant files in trial_file folder
#    i.e. not taking into account files that start with '.'

def myListDir(directory):
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]
#---------------------------------------------------------------


#    Experiment parameters
testLanguage = 'French'
testID = 'naturalness'
date = datetime.datetime.now()

trialFilePath = os.path.dirname(__file__)+'/trial_files/'
trialFileList = myListDir(trialFilePath)
subjNr = len(trialFileList)+1    #    If the experiment is interrupted before the end, replace by subjNr= with the correct subject number

#    Generates a new file in trial_files folder with randomised order of trials
randomiseFiles.main(subjNr,subjNr,testID,testLanguage)

#    Set directory paths
imPath = os.path.dirname(__file__)+'/images/'
soundPath = os.path.dirname(__file__)+'/sounds/'
resultsFile = os.path.dirname(__file__)+'/results/subj'+str(subjNr)+'_'+testLanguage+'_'+date.strftime('%y%m%d_%H.%M')+'.csv'        # writes a new csv file in which to save the experiment results

#    Screen / mouse parameters
win = visual.Window([1440,900],fullscr=True,color="lightgray", units='norm')
mouse = event.Mouse()

#    Ratio for image scaling
screenRatio = (float(win.size[1])/float(win.size[0]))

#    Parameters for rating scale
labelSize = 0.07
length = 0.5
lineLoc = -0.5
lowerLimit = 1
upperLimit = 100
labelLeftText1 = ''
labelLeftText2 = None
labelRightText1 = ''
labelRightText2 = None
start = None


####################################
#             Functions            #
####################################


#    Function to read the trialFile that has been made for the subject 
#    and returns pairs of audio files for each trial

def getTrials(subjNr = None, outfile = resultsFile, trialFilePath = trialFilePath, lang = testLanguage):
    trialFile = trialFilePath+lang+'_subj'+str(subjNr)+'.csv' 
    
    with open(trialFile, 'rb') as ftrials :
        reader = csv.reader(ftrials)
        trialList = list(reader)

    outList = []
    outHeaders = trialList[0]
    outHeaders.extend(('file', 'response', 'responseTime', 'timesPlayed'))

    with open(outfile, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = outHeaders)
        writer.writeheader()

    trialList = trialList[1::]
    stimList = []

    for line in trialList:
        audioFile = [ str(line[0]) + str(line[1]) + str(line[2]) + str(line[3]) + str(line[4]) + '.wav' ]
        stimList.append(audioFile)

    return stimList,trialList


#-------------------------------------------
#    Function to show texts for instructions,
#    between blocks, 
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


#----------------------------------------
#    Function to draw all objects at once

def drawObjects():
    play.draw()
    square.draw()
    instruction.draw()
    line.draw()
    labelLeft1.draw()
    labelRight1.draw()
    if labelLeft2 and labelRight2 :
        labelLeft2.draw()
        labelRight2.draw()
        labelLeft3.draw()
        labelRight3.draw()
    next.draw()
    nextBox.draw()
    if startClicks == True:
        marker.draw()
    if setWarning == True :
        warning.draw()


####################################
#            Play sounds           #
####################################


instruction = visual.TextStim(win, units='norm', text='Please listen to the sentence by clicking the play button below and rate how natural / artificial the voice sounds', color='black', height=labelSize, pos=(0,0.5), alignHoriz='center')

warning = visual.TextStim(win, units='norm', text='Please listen to the sentence before giving your response', color='red', height=0.8*labelSize, pos=(0,-0.65), alignHoriz='center')

play = visual.ImageStim(win, image=imPath+'play2.png', units='norm', size = (0.2*screenRatio,0.2), pos=(0,0.2))

square = visual.ShapeStim(win, fillColor = None
                            , lineColor = None
                            , opacity = 1
                            , units = 'norm'
                            , vertices=[ (-0.12, 0.1)
                                       , (-0.12, 0.3)
                                       , ( 0.12, 0.3)
                                       , ( 0.12, 0.1)
                                        ]
                            )
                     



####################################
#           Rating scale           #
####################################

#    Rating scale
labelLeftText1 = 'not at all natural'
labelRightText1 = 'very natural'

labelLeftText2 = 'very artificial'
labelRightText2 = 'not at all artificial'

def setMarker(value=None):
    scaleRange = float(upperLimit - lowerLimit)
    leftVal = -(line.size[0] / 2.0)
    return (((value - lowerLimit) / scaleRange) * line.size[0]) + leftVal

if start == None:
    start = lowerLimit + ((upperLimit - lowerLimit) / 2)                   #    Start at the middle

xPos = 0
line = visual.ImageStim(win, image=imPath+'line.png', units='norm', size=(2*length,0.03), pos=(0.0,lineLoc))
marker = visual.ImageStim(win, image=imPath+'marker2.png', units='norm', size=(0.03,0.09), pos=(setMarker(start),lineLoc))

labelLeft1 = visual.TextStim(win, units='norm', text=labelLeftText1, color='black', height=0.8*labelSize, pos=(-(length+0.2),lineLoc+0.1))
labelRight1 = visual.TextStim(win, units='norm', text=labelRightText1, color='black', height=0.8*labelSize, pos=((length+0.2),lineLoc+0.1))

labelLeft2 = visual.TextStim(win, units='norm', text=labelLeftText2, color='black', height=0.8*labelSize, pos=(-(length+0.2),lineLoc-0.1))
labelRight2 = visual.TextStim(win, units='norm', text=labelRightText2, color='black', height=0.8*labelSize, pos=((length+0.2),lineLoc-0.1))

labelLeft3 = visual.TextStim(win, units='norm', text='/', color='black', height=0.8*labelSize, pos=(-(length+0.2),lineLoc))
labelRight3 = visual.TextStim(win, units='norm', text='/', color='black', height=0.8*labelSize, pos=((length+0.2),lineLoc))


#    Next button
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



####################################
#         Start experiment         #
####################################


showText(fileName = "intro.txt")        #    Instructions
showText(fileName = "practice.txt")             #    Practice trials

totalTrials = len(stimList) - 3    
counter = 0


#    Loop per trial
for trialNr in stimList : 
    next.setImage(imPath+'next_press.png')
    voice = sound.Sound(value=soundPath+trialNr[0])
    timesPlayed = 0
    endTrial = False
    startClicks = False
    setWarning = False
    startTime = time.getTime()
   
    while (not endTrial):
        drawObjects()
        win.flip()
        while mouse.getPressed()[0] == 0:
            drawObjects()
            win.flip()

        if mouse.isPressedIn(square) :
            timesPlayed += 1
            setWarning = False
            voice.play()
        
        elif mouse.isPressedIn(marker):
            startClicks = True
            while mouse.getPressed()[0] == 1:
                mouseX, mouseY = mouse.getPos()
                marker.setPos((min(max(mouseX, -length), length), marker.pos[1]))
                next.setImage(imPath+'next.png')
                drawObjects()
                win.flip()

        elif mouse.isPressedIn(line):
            if timesPlayed == 0 :
                setWarning = True
                drawObjects()
                win.flip()
            else :
                startClicks = True
                mouseX, mouseY = mouse.getPos()
                marker.setPos((min(max(mouseX, -length), length), marker.pos[1]))
                next.setImage(imPath+'next.png')
                drawObjects()
                win.flip()
            
        if mouse.isPressedIn(nextBox) and startClicks == True:
            endTime = time.getTime()
            rt = endTime - startTime
            rt = round(rt, 2)
            response = round((marker.pos[0] / (2 * length) + 0.5) * 100)
            if response < lowerLimit: response = lowerLimit
            elif response > upperLimit: response = upperLimit
            print 'your rating is '+str(response)
            print response, rt
            endTrial = True
            win.flip()
            core.wait(0.5)
        while mouse.getPressed()[0] == 1:
            drawObjects()
            win.flip()
            core.wait(0.1)
            

    #    Write results to file
    trialList[counter].extend(( trialNr[0], response, rt, timesPlayed))
    with open(resultsFile, 'a') as fout :
        writer = csv.writer(fout)
        writer.writerow(trialList[counter])

    counter += 1   

    if counter == 3:
        showText(fileName = "start_test.txt")

    elif counter == totalTrials/2 + 3 :
        showText(fileName = "pause.txt")


#End of experiment
showText(fileName = "outro.txt")


# Close Python
win.close()
core.quit()
sys.exit()

