# Randomisation code for the implicit/explicit experiment
##### Laura Rachman 
##### May 2017



This code creates lists of trials in a randomised order for the implicit/explicit experiment. 

This code randomizes the trials such as:

- There is at least one neutral stimulus in each pair
- There is as many happy-neutral, neutral-neutral and sad-neutral pairs
- You obtain the same number of stimuli pairs in the 4 conditions of the experiment: Same other, Same self, Different other and Different self

This script creates two lists for each subject: one for the implicit task and another for the explicit task (see [Implicit Explicit experimentation](https://github.com/creamlab/Cream_Code/tree/master/Implicit%20Explicit)).

[By forking this folder](https://github.com/creamlab/...), you'll be able to create files of randomized trials for 21 different subjects, male or female. You do not need any stimulus to run the code. 


## Folder you need to have


- /trial_lists : this folder will contain the randomisation list (.csv file) for each subject and for each condition. 

## Input

#### Subjects

The code will ask:

- a subject number
- a subject gender

Make sure the subject number is defined in your code and that the gender corresponds.

	27  #    Define stimulus information
    28 		if gender == 'female':
    29     			speakerNr = [1,2,3,5,10,11,14,15,20,21]
    30 		elif gender == 'male':
    31     			speakerNr = [4,6,7,8,9,12,13,16,18,19]
## Outputs

#### Trial files
.csv files containing the trials files content for each subject and for each task.

Format : id\_**testID**\_s**SubjectNumber**\_**Date**\_**Hour**.csv (i.e. *id\_explicit\_subj01\_171005\_142536.csv* for the explicit task of the subject n°1, created the 5th October 2017 at 2 hours 25 minutes and 36 seconds pm)

![Trial File](https://github.com/creamlab/Cream_Code/blob/master/Images/TrialFile.png)

#### Stimuli
No stimulus is created but the trial file will contain the name of your future stimuli ([Implicit Explicit experimentation](https://github.com/creamlab/Cream_Code/tree/master/Implicit%20Explicit)). 

The format for the future stimuli is defined in the code as : s**SpeakerNumber**\_w**WordNumber**\_**Emotion**.wav (i.e. *s901\_w15\_s.wav* for speaker n°1, word n°15, sad emotion) 

# 




