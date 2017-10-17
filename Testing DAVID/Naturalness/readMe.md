# Testing the naturalness of voices modified with DAVID
##### Laura Rachman 
laura.rachman@ircam.fr
##### 2015
 
This experiment has been designed to test the naturalness of voices once they were modified with our DAVID software. Indeed, DAVID is able to connotate the voices with an emotion (happy, sad, angry...) by modifying the pitch, inflection, filter... of the voices (see [our website](http://cream.ircam.fr/?p=44) to freely download and use DAVID).

In this experiment, the subject listens to a sound, as many times as he wants, and immediately rate the naturalness of the sound on a scale.  

In order to do so, the participant can judge the control and the affiliation of the left player on the right player. This is done after each duet he heard, on 2 different scales.

[By downloading this folder](https://github.com/creamlab/Cream_Code/archive/master.zip) you'll be able to launch the experiment until the end of the pactice trials. To continue, you must add your own stimuli or contact us to have ours (See Stimuli section for the syntax needed).


**With this code, you can make:**

	A randomisation file of the trials for each subject
	Audio stimuli presentation listenable as many times as the subject wants
	Simple continuous rating scale for 1 to 100
	1 block of 75 trials with a pause at the middle of the experiment

## Folders you need to have

- /images : images use during the experiment
- /sounds : audio presented to the participant. 
- /results : will contain one .csv file with each subject's results.
- /trial\_files : will contain one .csv file for each subject. Each file is the list of randomised trials for the experiment.

## Inputs

### Texts (in french)
- intro.txt : instructions given at the beginning of the experiment
- practice.txt : announcement of the 3 practice trials
- start_test.txt : beginning of the experiment
- pause.txt : annoncement of the pause
- outro.txt : end of the experiment


### Stimuli
Audio presented to the subject. Format : **SpeakerSex SpeakerNumber SentenceNumber Emotion Intensity**.wav(i.e. *F14h2.wav* for the female speaker n°1, 4th sentence, modified with the 2nd intensity of the happy effect).

For the practice trials, the speaker sex is P and the the speaker number 0. 

Each speaker says 4 different sentences, modified by DAVID with 3 types of effects : happy, sad or angry. 

## Outputs
### Trial files
Files containing the randomised order of stimuli presentation for each subject. They are created by the randomiseFiles.py code, called in the experiment script. It creates the randomised files at the beginning of the experiment with a subject number. This number is incremented from the number of files already created in the trial_files folder. 

In each file, a sample of the all the possible audio is randomised. The sample is selected in order to have the same number of trials for :

- each speaker (sex and number)
- each sentence
- each emotion (type and intensity)

Format : **TestLanguage**\_subj**SubjectNumber**.csv (i.e. *French\_subj6.csv* for the french subject n°6)

![Trial File](https://github.com/creamlab/Cream_Code/blob/master/Images/TrialFile3.png)
### Results
.csv files containing the subject's answers for the entire experiment.

Format : subj**SubjectNumber**\_**TestLanguage**\_**Date**\_**Hour**.csv (i.e. *subj3\_French\_151013\_12.43.csv* for the french subject n°3 doing the experiment the 13th October 2015 at 12.43 pm)

![Results File](https://github.com/creamlab/Cream_Code/blob/master/Images/Results3.png)

## Warnings

Python can return an error of this type :

	Fatal Python error: (pygame parachute) Segmentation Fault
	
You can try by changing 'pygame' into 'pyo' in these lines to solve the problem:

	17 from psychopy import prefs
	18 prefs.general['audiolib']=['pygame']
