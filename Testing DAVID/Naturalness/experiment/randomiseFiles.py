# coding=utf-8

#----------------------------------------------------------------------#
#                          Randomisation code                          #
# For the naturalness/intensity/emotion experiments on modified voices #
#                          Laura Rachman _ 2015                        #
#----------------------------------------------------------------------#


#   Makes a trial list given a subject code and a seed for the random generator.

#   The function makes, shuffles and writes a trial list into a file
#   Subject number is used to write the file and seed is used for pseudorandomisation


import random
import numpy as np


def main(subjNr,seed, testID = None, testLanguage = None):

    #    Stimulus information
    speakerSex = ['M','F']
    speakerNr = ['1','2','3']
    sentenceNr = ['1', '4', '5', '6']          #    Sentence numbers
    emoType = ['n','h','s','a']                #    n=neutral, h=happy, s=sad, a=afraid
    intensity = ['1', '2', '3']                #    Intensity level of the emotions: 1=low, 2=medium, 3=high

    separator = ','

    testFile = open('trial_files/'+'/'+testLanguage+'_subj' + str(subjNr) + '.csv', 'w')

    #    Column headers
    print >> testFile, separator.join(("speakerSex", "speakerNr", "sentenceNr", "emoType", "intensity"))

    #    Get different seed per subject...
    random.seed(seed)
    seed = int(seed)
 
    #    ...Test type... 
    if testID == 'emotion' :
        seed += 10
    elif testID == 'naturalness' :
        seed += 40
    elif testID == 'intensity' :
        seed += 70
    else : 
        seed = seed

    #    ...And language
    if testLanguage == 'English' : 
        seed += 100
    elif testLanguage == 'French' :
        seed += 200
    elif testLanguage == 'Swedish' :
        seed += 300
    elif testLanguage == 'Japanese' :
        seed += 400
    else : 
        seed = seed

    #    Generate 3 practice trials
    completeList = []
    completeList.append(separator.join(('P','0','1','h','9')))
    completeList.append(separator.join(('P','0','2','s','9')))
    completeList.append(separator.join(('P','0','4','a','9')))
    
    trialList = []
    #    Trial randomization for the emotion test
    if testID == 'emotion':
        for currentSpeakerSex in speakerSex:
            for currentSpeakerNr in speakerNr:
                sentenceList = []
                for i in range(6):                  #    Shuffles sentence numbers and repeats the list 6 times in a new sentenceList
                    random.shuffle(sentenceNr)
                    sentenceList.extend(sentenceNr)
                
                types = np.array(list(emoType * 6)).reshape(6,len(emoType))    
                emoList = []
                for j in range(len(emoType)):       #    Makes a list with each emotion type repeated 6 times
                    emoList.extend(types[:,j])
                
                levels = np.array(list(intensity * 2)).reshape(2,len(intensity))    
                levelList = []
                for k in range(len(intensity)):     #    Makes a list with each intensity level repeated 2 times
                    levelList.extend(levels[:,k])
                for l in range(2):                  #    Get 4 repetitions of the list
                    levelList.extend(levelList)

                for index in range(len(sentenceList)):
                    trialList.append(separator.join((currentSpeakerSex, currentSpeakerNr, sentenceList[index], emoList[index], levelList[index])))

    #    Trial randomisation for naturalness and intensity tests            
    else:                                       
        intensity.extend('0')                       #    Add '0' to list of intensity levels for the naturally pronounced emotions
        emoType = ['h', 's', 'a']                   #    No neutral sentences
        for currentSpeakerSex in speakerSex:
            for currentSpeakerNr in speakerNr:
                sentenceList = []
                for i in range(3):
                    random.shuffle(sentenceNr)
                    sentenceList.extend(sentenceNr)

                types = np.array(list(emoType * 4)).reshape(4,len(emoType))
                emoList = []
                for j in range(len(emoType)):
                    emoList.extend(types[:,j])

                levelList = []
                for k in range(3):
                    levelList.extend(intensity)

                for index in range(len(sentenceList)):
                    trialList.append(separator.join((currentSpeakerSex, currentSpeakerNr, sentenceList[index], emoList[index], levelList[index])))

    #    Shuffle all the trials and print in the file
    random.shuffle(trialList)
    completeList.extend(trialList)
    for currentTrialList in completeList:
        print >>testFile, currentTrialList

                     
#    Running the file as a script (instead of importing it) to create a sample file
if __name__ == "__main__":
    trialList = main(str(subjNr),subjNr, testID, testLanguage)
