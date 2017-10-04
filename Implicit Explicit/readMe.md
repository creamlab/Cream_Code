# Implicit/Explicit _ Self and other voices recognition
##### Laura Rachman 
laura.rachman@ircam.fr
##### May 2017

# 

In this experience, the subject listens to 2 voices and has to determine whether or not these two were pronounced by the same speaker. In order to do so, he has to answer the question 'Are these two words produce by the same speaker?' or 'Did you heard your own voice?' with two different answers 'yes' or 'no'.

The experiment is divided in 2 parts. In the first, we ask if the voices come from the same speaker (implicit task). In the 2nd, we tell the participant he's one of the speakers and ask now if he's hearing his own voice (explicit task).


[By forking this folder](https://github.com/creamlab/...) you'll be able to launch the experiment for a female subject n°1 until the end of the practice session. To continue, you must add your own stimuli or contact us to have ours.

**With this code, you can make:**

	Dialog box to collect subject's informations
	2 audio stimuli presentation
	Yes/no question
	4 blocks of 36 trials

## Folders you need to have

- /images : images use during the experimentation
- /stimuli : audio presented to the participant. 
- /results : will contain .csv files of a subject's results
- /trail\_lists : .csv files containing the trials file for each subject [1](https://github.com/creamlab/...)

## Inputs

#### Texts (in french)
- intro.txt : instructions
- practice.txt : announcement of practice trials
- end_practice.txt : announcement of the end of practice and beginning of the experiment
- pause.txt : enf of the block
- outro.txt : end of the task and move on the next one
- outro_end.txt : end of the experiment



#### Stimuli
Audio presented to the subject.

Format : s**SpeakerNumber**\_w**WordNumber**\_**Emotion**.wav (i.e. *s901\_w15\_h.wav* for speaker n°1, word n°15, happy emotion) 

Except for the practice files where emotion is written in full : *neutral*

#### Trials files
Files containing the order of stimuli presentation for each subject.

Produced by a randomisation code [1](https://github.com/creamlab/...)

Format : id\_**testID**\_s**SubjectNumber**\_**Date**\_**Hour**.csv (i.e. *id\_implicit\_subj01\_171003\_15.43.csv* for the implicit task of subject n°1, created the 3rd October 2017 at 3.43 pm)

![Trial File](https://github.com/creamlab/...TrialFile.png)

## Outputs

#### Results
.csv files containing the trials files content and the subject's answers

Format : id\_**testID**\_s**SubjectNumber**\_**Date**\_**Hour**.csv (i.e. *id\_explicit\_subj01\_171004\_14.12.csv* for subject n°1 doing the explicit task the 4th October 2017 at 2.12 pm)

![Results File](https://github.com/creamlab/...Results.png)
#### Log files
. log files are produce and collect all the actions produced during the experience

Format : sub**SubjectNumber**.log

Because they're named only by the subject number, they are overwritten if you have to subject with the same number.

![Log File](https://github.com/creamlab/...Log.png)

1: [Randomisation code](https://github.com/creamlab/...)


