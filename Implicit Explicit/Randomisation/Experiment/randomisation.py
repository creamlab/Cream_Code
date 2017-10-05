# coding=utf-8

# ---------------------------------------------------------------------------- #
# Implicit and explicit identity recognition task using DAVID transformations  #
#                           Laura Rachman - May 2017                           #
#           Generation of stimulus lists randomized for each subject           #
# ---------------------------------------------------------------------------- #

import random
import datetime
import pandas as pd
import numpy as np


#    Function to make shuffles, and write a trial list to file.
#    Subject number is used to write the file.
#    Seed is used for pseudorandomization.

def main():

#    Get number to save later
    subject = raw_input("Subject number: ")
    gender = raw_input("Gender: ")   
    subjNr = int(subject)


#    Define stimulus information
    if gender == 'female':
        speakerNr = [1,2,3,5,10,11,14,15,20,21]
    elif gender == 'male':
        speakerNr = [4,6,7,8,9,12,13,16,18,19]

    speakerNr.remove(subjNr)
    random.shuffle(speakerNr)
    otherA = speakerNr[0]
    otherB = speakerNr[1]
    
    npoints = 12         #    Number of stimuli per condition
    
    expList = pd.DataFrame()
    
    cond = ['diffOther', 'diffSelf', 'sameOther', 'sameSelf']
    
    for currcond in cond:
        if currcond == 'diffOther':
            speaker1 = 'otherA'
            speaker2 = 'otherA'
            speaker3 = 'otherB'
            speaker4 = 'otherB'
        elif currcond == 'diffSelf':
            speaker1 = 'self'
            speaker2 = 'self'
            speaker3 = 'otherA'
            speaker4 = 'otherB'
        elif currcond == 'sameOther':
            speaker1 = 'otherA'
            speaker2 = 'otherB'
            speaker3 = 'otherA'
            speaker4 = 'otherB'
        elif currcond == 'sameSelf':
            speaker1 = 'self'
            speaker2 = 'self'
            speaker3 = 'self'
            speaker4 = 'self'
    
        words1 = range(1,21)
        words2 = range(1,21)
        words3 = range(1,21)
        words4 = range(1,21)
        
        random.shuffle(words1)
        random.shuffle(words2)
        random.shuffle(words3)
        random.shuffle(words4)
        
        wordList = words1 + words2 + words3 + words4[0:npoints]
        
        stim1 = pd.Series(wordList[0::2],name='stim1')
        stim2 = pd.Series(wordList[1::2],name='stim2')
        
        stimList = pd.DataFrame([stim1,stim2]).transpose()
        
        emo1 = np.repeat(['n'],3*npoints)
        emo2 = np.repeat(['n', 'h', 's'],npoints)
        
        emoList1 = pd.Series(emo1,name='emo1')
        emoList2 = pd.Series(emo2,name='emo2')
        
        id1 = np.array([speaker1,speaker2])
        id1 = np.tile(id1,3*npoints)
        id2 = np.array([speaker3,speaker4])
        id2 = np.tile(id2,3*npoints)
        
        idList1 = pd.Series(id1,name='id1')
        idList2 = pd.Series(id2,name='id2')
        
        if currcond == 'diffSelf':
            swap_emo = np.repeat([1,-1],int(0.5*npoints))
            swap_emo = np.tile(swap_emo,3)
            swapList1 = pd.Series(swap_emo,name='swap1')
            swapList2 = pd.Series(swap_emo,name='swap2')
        elif currcond == 'sameOther':
            swap_emo = np.repeat([1,-1],int(0.5*npoints))
            swap_emo = np.tile(swap_emo,3)
            swapList1 = pd.Series(swap_emo,name='swap1')
            swap_id = np.repeat([1,-1],int(2))
            swap_id = np.tile(swap_id,int(0.5*npoints*3.0))
            swapList2 = pd.Series(swap_id[0:(3*npoints)],name='swap2')
        else:
            swap_emo = np.array([1,-1]*int(3*0.5*npoints))
            swapList1 = pd.Series(swap_emo,name='swap1')
            swap_id = np.repeat([1,-1],int(2))
            swap_id = np.tile(swap_id,int(0.5*npoints*3.0))
            swapList2 = pd.Series(swap_id[0:(3*npoints)],name='swap2')

        
        condList = pd.Series([currcond]*3*npoints,name='condition')
        
        stimList = stimList.join(emoList1)
        stimList = stimList.join(emoList2)
        stimList = stimList.join(idList1)
        stimList = stimList.join(idList2)
        stimList = stimList.join(swapList1)
        stimList = stimList.join(swapList2)
        stimList = stimList.join(condList)
                
        idx_emo = (stimList['swap1'] == 1)
        idx_id = (stimList['swap2'] == -1)
        
        stimList.loc[idx_emo,['emo1','emo2']] = stimList.loc[idx_emo,['emo2','emo1']].values
        stimList.loc[idx_id,['id1','id2']] = stimList.loc[idx_id,['id2','id1']].values
                    
        expList = expList.append(stimList)
    expList = expList.reset_index()

    currtime = ('{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now()))
           
    separator = ','

#    IMPLICIT

#    Trial list self/other test
    trialList = []
    selfFile = open('trial_lists/id_implicit_s' + format(subjNr,'02') + '_' + currtime + '.csv', 'w')
    print selfFile

#    Print column headers to the file
    print >> selfFile, separator.join(("stimulus1", "stimulus2", "word1", "word2", "emotion1", "emotion2", "speaker1", "speaker2", "speaker1_ID", "speaker2_ID", "condition", "participantID", "gender"))
                                       
               
    for i in range(len(expList)):
        idA = expList.iloc[i]['id1']
        idB = expList.iloc[i]['id2']
        if idA == 'otherA':
            currSpeaker1 = '9'+format(otherA,'02')
        elif idA == 'otherB':
            currSpeaker1 = '9'+format(otherB,'02')
        elif idA == 'self':
            currSpeaker1 = '9'+format(subjNr,'02')
            
        if idB == 'otherA':
            currSpeaker2 = '9'+format(otherA,'02')
        elif idB == 'otherB':
            currSpeaker2 = '9'+format(otherB,'02')
        elif idB == 'self':
            currSpeaker2 = '9'+format(subjNr,'02')
        
        currWord1 = format(expList.stim1[i],'02')       
        currWord2 = format(expList.stim2[i],'02')       
        currEmo1 = expList.emo1[i]
        currEmo2 = expList.emo2[i]
        
        currStim1 = 's' + currSpeaker1 + '_w' + currWord1 + '_' + currEmo1 + '.wav'
        currStim2 = 's' + currSpeaker2 + '_w' + currWord2 + '_' + currEmo2 + '.wav'
                
        trialList.append(separator.join((currStim1,currStim2,currWord1,currWord2,currEmo1,currEmo2,expList.id1[i],expList.id2[i],currSpeaker1,currSpeaker2,expList.condition[i],str(subjNr),gender)))


    random.shuffle(trialList)
    for currTrial in trialList:
        print >>selfFile, currTrial

#    EXPLICIT

    expFile = open('trial_lists/id_explicit_s' + format(subjNr,'02') + '_' + currtime + '.csv', 'w')
    
#    Print column headers to the file
    print >> expFile, separator.join(("stimulus1", "stimulus2", "word1", "word2", "emotion1", "emotion2", "speaker1", "speaker2", "speaker1_ID", "speaker2_ID", "condition", "participantID", "gender"))
    
    random.shuffle(trialList)
    for currTrial in trialList:
        print >>expFile, currTrial



#   Running the file as a script (instead of importing it) creates a sample file
if __name__ == "__main__":
    main()
