# Influence of time shift and detune on judgments of affiliation/control in improvised duets
##### Jean-Julien Aucouturier 
jean-julien.aucouturier@ircam.fr
##### 2016
 

In this experiment, the subject listens to an improvised duet between 2 instrumental players. Each player is heard in one distinct hear. The participant has to judge if the left player is dominating or submitting the right one (control), and if he tries to be warm with the other or if he's hostile and excludes him (affiliation). 

In order to do so, the participant can judge the control and the affiliation of the left player on the right player. This is done after each duet he heard, on 2 different scales.

[By downloading this folder](https://github.com/creamlab/Cream_Code/archive/master.zip) you'll be able to launch the experiment until the end of the instructions. To continue, you must add your own stimuli or contact us to have ours (See Stimuli section for the syntax needed).


**With this code, you can make:**

	Dialog box to collect subject's informations
	Audio stimuli presentation with pictures
	2 categorial rating scales for different judgments from 1 to 9
	2 blocks of 15 trials with a 2 minutes pause

## Folders you need to have

- /images : images use during the experiment
- /sounds : audio presented to the participant. 
- /results : will contain one .csv file with one subject's results. One file contains both blocks of the experiment
- /trial\_files : will contain 2 .csv files for each subject. Each file is the list of randomized trials for one block

## Inputs

### Texts (in french)
- intro/affiliation/control/mix/intro_3.txt : instructions given at the beginning of the experiment in this order 
- pause2/1/0.txt : annoncement of the pause and countdown of the 2 minutes
- outro.txt : end of the experiment


### Stimuli
Audio presented to the subject. Each audio is presented 2 times during the experiment : one version is the original duet and the other is a modified (detune and/or time shift) version

Format : N°_N°.**modification**.wav(i.e. *7_3.M.wav* for the modified version of the 7_3 audio).

To run the experiment, please make sure that the N°_N° of your audio correspond to the lists created in the code (here separated in 3 lists, according to the instructions given to the players during the recording) or change these lines:

	54 song_aff_down = ['1_1','2_9','5_5','5_9','5_10']
	55 instruments_aff_down_A = ['Piano', 'Piano','Alto', 'Alto', 'Violon']
	56 instruments_aff_down_B = ['Saxophone','Saxophone','Violon', 'Violon','Alto']

	58 song_con_down = ['1_7','1_7_2','3_9','4_8','3_6']
	59 instruments_con_down_A = ['Piano', 'Piano','Basson', 'Saxophone', 'Saxophone']
	60 instruments_con_down_B = ['Saxophone','Saxophone','Saxophone', 'Piano','Basson']

	62 song_con_up = ['3_7','7_3','8_2','9_10','10_5']
	63 instruments_con_up_A = ['Basson', 'Guitare','Saxophone', 'Alto', 'Flute']
	64 instruments_con_up_B = ['Saxophone','Clarinette','Contrebasse', 'Contrebasse','Alto']

In the sounds folder, you can find 2 audio named 1_1.NM.wav and 1_1.M.wav. These are a piano/saxophone duet in both modified and non modified versions. They are here to illustrate what the duet we used look like but will not allow you to run the experiment.

## Outputs
### Trial files
Files containing the randomized order of stimuli presentation for each subject. They are created at the beginning of the experiment with the informations given in the toolbox.

2 trial files are produced for each participant, corresponding to the 2 blocks of the experiment. In each file, all the audio are presented in a randomized order in the original version or in the modified one. The other version of each audio will be presented in the second block of the experiment, with another randomized order.

Format : trialList\_subj**SubjectNumber**\_**BlockNumber**\_**Date**\_**Hour**.csv (i.e. *trialList\_subj2\_1\_160723\_15.25.csv* for the 1st block of the subject n°2, created the 23rd July 2016 at 3.25 pm)

![Trial File](https://github.com/creamlab/Cream_Code/blob/master/Images/TrialFile2.png)
### Results
.csv files containing the subject's answers for the 2 blocks.

Format : subj**SubjectNumber**\_ratings\_**Date**\_**Hour**.csv (i.e. *subj3\_ratings\_160725\_09.12.csv* for subject n°3 doing experiment the 25th July 2016 at 9.12 am)

![Results File](https://github.com/creamlab/Cream_Code/blob/master/Images/Results2.png)

## Warnings

Python can return an error of this type :

	Fatal Python error: (pygame parachute) Segmentation Fault
	
You can try by changing 'pygame' into 'pyo' in these lines to solve the problem:

	17 from psychopy import prefs
	18 prefs.general['audiolib']=['pygame']