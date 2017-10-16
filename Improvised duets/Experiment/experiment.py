# coding=utf-8

#--------------------------------------------------------------------------#
#  Influence of time shift and detune on judgments of affiliation/control  #
#                            in improvised duets                           #
#                                JJA - 2016                                #
#--------------------------------------------------------------------------#


import sys
import os
import unicodecsv as csv
import codecs
import datetime
import random
import webbrowser
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual,gui,event,core,sound


#---------------------------------------------------------
#    Creation of a class to define all the graphic objects

class MyButton(object):
    """Encapsulates all graphic objects for a button"""
    def __init__(this, win, x_pos, y_pos, img, title=None):
        this.button = visual.ImageStim(win, image=img_path+img, units='norm', size = (0.2*screen_ratio,0.2), pos=(x_pos,y_pos))
        this.box = visual.ShapeStim(win, fillColor = None, lineColor = 0, opacity = 0, units = 'norm', vertices=[ (x_pos-0.1, y_pos-0.1), (x_pos-0.1, y_pos+0.1),(x_pos+0.1, y_pos+0.1), (x_pos+0.1,y_pos-0.1)])
        this.title = visual.TextStim(win, units='norm', text=title, color='black', height=0.07, pos=(x_pos,y_pos-0.1))
        
    def setImage(this, img):
        this.button.setImage(img_path+img)

    def draw(this):
        this.button.draw()
        this.box.draw()
        this.title.draw()

    def disable(this, img = None):
        this.disabled = True
        if(img!=None):
            this.setImage(img)

    def enable(this, img = None):
        this.disabled = False
        if(img!=None):
            this.setImage(img)
#---------------------------------------------------------


#    Lists of stimuli distributed according to the instructions given to the players during the recording

song_aff_down = ['1_1','2_9','5_5','5_9','5_10']
instruments_aff_down_A = ['Piano', 'Piano','Alto', 'Alto', 'Violon']
instruments_aff_down_B = ['Saxophone','Saxophone','Violon', 'Violon','Alto']

song_con_down = ['1_7','1_7_2','3_9','4_8','3_6']
instruments_con_down_A = ['Piano', 'Piano','Basson', 'Saxophone', 'Saxophone']
instruments_con_down_B = ['Saxophone','Saxophone','Saxophone', 'Piano','Basson']

song_con_up = ['3_7','7_3','8_2','9_10','10_5']
instruments_con_up_A = ['Basson', 'Guitare','Saxophone', 'Alto', 'Flute']
instruments_con_up_B = ['Saxophone','Clarinette','Contrebasse', 'Contrebasse','Alto']


####################################
#             Functions            #
####################################

#----------------------------------------------------------
#    Generation of the randomisation files for each subject
#    Each file = one block = all the stimuli modified or not

def generate_trial_files(subject_number):
    seed = time.getTime()
    random.seed(seed)
    separator = ','

    song_numbers = song_aff_down + song_con_up + song_con_down
    song_conditions = ['A-']*5 + ['C+']*5 + ['C-']*5
    song_instruments_A = instruments_aff_down_A + instruments_con_up_A + instruments_con_down_A
    song_instruments_B = instruments_aff_down_B + instruments_con_up_B + instruments_con_down_B
    
    #    Randomly assign one of Non-Modified NM or Modified M stimuli in the 2 blocks
    #    Return an array of 2 file names
    manips = ['NM','M']
    song_manipulations_1 = []
    song_manipulations_2 = []
    for song in song_numbers : 
        random.shuffle(manips)
        song_manipulations_1.append(manips[0])
        song_manipulations_2.append(manips[1])

    trial_files = []
    for block_counter, manipulations in zip([1,2],[song_manipulations_1,song_manipulations_2]): 
        trial_file = 'trial_files/trialList_subj' + str(subject_number) + '_' + str(block_counter) + '_' + date.strftime('%y%m%d_%H.%M')+'.csv'
        trial_files.append(trial_file)
        with codecs.open (trial_file, "w", "utf-8") as fid :
            print >> fid, separator.join(("Song", "Instr_A", "Instr_B", "Cond","Manip","SongFile"))
            trial_list = []
            for song, inst_A, inst_B, cond, manip in zip(song_numbers,song_instruments_A, song_instruments_B,song_conditions, manipulations):
                song_file = song+'.'+manip+'.wav'
                trial_list.append(separator.join((song, inst_A, inst_B, cond, manip, song_file)))
            random.shuffle(trial_list)
            for trial in trial_list:
                print >>fid, trial
    return trial_files
#----------------------------------------------------------


def read_trials(trial_file): 
    with open(trial_file, 'rb') as fid :
        reader = csv.reader(fid)
        trials = list(reader)
    return trials[1::]

def get_audio_file(trial): 
    audio_file = trial[5]
    return audio_file


#--------------------------------------------------------------------
#    Creation of the results files and writing of the subject answers

def generate_result_file(subject_number):
    result_file = os.path.dirname(__file__)+'/results/subj'+str(subject_number)+'_ratings_'+date.strftime('%y%m%d_%H.%M')+'.csv'        
    result_headers = ['SubjNr','Sex','Age','Date','Song', 'Cond','Manip','SongFile','Affiliation','Control']
    with open(result_file, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = result_headers)
        writer.writeheader()
    return result_file

def write_preference_result(result_file, subject_number,sex,age,date,song, cond, manip, song_file, affiliation, control):
    with open(result_file, 'a') as fid :
        writer = csv.writer(fid, encoding="utf-8")
        writer.writerow([subject_number,sex,age,date,song, cond, manip, song_file, affiliation, control])


#----------------------------------------------------------------------------
#    Functions to show the different texts and pictures during the experiment

def show_text_and_wait(file_name):
    event.clearEvents()
    with codecs.open (file_name, "r", "utf-8") as file :
        message = file.read()
	text_object = visual.TextStim(win, text = message, color = 'black')
    text_object.height = 0.05
    text_object.draw()
    win.flip()
    while True :
        if len(event.getKeys()) > 0: 
            core.wait(0.2)
            break
        event.clearEvents()
        core.wait(0.2)
    	text_object.draw()
        win.flip()


def show_text(file_name):
    with codecs.open (file_name, "r", "utf-8") as file :
        message = file.read()
    text_object = visual.TextStim(win, text = message, color = 'black')
    text_object.height = 0.05
    text_object.draw()
    win.flip()


def show_text_and_pics_and_wait(file_name, pic1, pic2):
    event.clearEvents()
    with codecs.open (file_name, "r", "utf-8") as file :
        message = file.read()
    text_object = visual.TextStim(win, text = message, color = 'black', pos = (0,0.5))
    text_object.height = 0.05
    pic1 = visual.ImageStim(win, image=img_path+pic1, units='norm', size = (0.5,0.4), pos=(-0.5,-0.1))
    pic2 = visual.ImageStim(win, image=img_path+pic2, units='norm', size = (0.5,0.4), pos=(0.5,-0.1))
    text_object.draw()
    pic1.draw()
    pic2.draw()
    win.flip()
    while True :
        if len(event.getKeys()) > 0: 
            core.wait(0.2)
            break
        event.clearEvents()
        core.wait(0.2)
        text_object.draw()
        pic1.draw()
        pic2.draw()
        win.flip()

#--------------------------------------------
#    Functions to show the different elements

def update_preference_gui():
    play_button.draw()
    sound_label.draw()
    instruction.draw()
    affiliation_scale.draw()
    affiliation_pic1.draw()
    affiliation_pic2.draw()
    control_scale.draw()
    control_pic1.draw()
    control_pic2.draw()
    win.flip()

def update_play_gui(): 
    trigger_instruction.draw()
    fixation.draw()
    instr_A_pic.draw()
    instr_B_pic.draw()
    win.flip()
   

####################################
#         Start experiment         #
####################################


#    Dialog box to collect subject informations : number, age, sex
subject_info = {u'Number':1, u'Pseudo':u'bob', u'Age':20, u'Sex': u'f/m'}
dlg = gui.DlgFromDict(subject_info, title=u'PREFERENCE')
if dlg.OK:
    subject_number = subject_info[u'Number']
    subject_pseudo = subject_info[u'Pseudo']
    age = subject_info[u'Age']
    sex = subject_info[u'Sex']    
    print sex
else:
    core.quit() 

date = datetime.datetime.now()
time = core.Clock()

#    Screen / mouse parameters
win = visual.Window([1990,1050],fullscr=True,color="lightgray", units='norm')
mouse = event.Mouse()

#    Ratio for image scaling
screen_ratio = (float(win.size[1])/float(win.size[0]))
           
#    Set directory paths
img_path = os.path.dirname(__file__)+'/images/'
sound_path = os.path.dirname(__file__)+'/sounds/'

#    Definition of the elements to show 

#      During sound
trigger_instruction = visual.TextStim(win, units='norm',color='black', height=0.05, pos=(0,0.5), alignHoriz='center')
fixation = visual.TextStim(win, units='norm', text=u"+",color='black', height=0.1, pos=(0,0), alignHoriz='center')
instr_A_pic = visual.ImageStim(win, units='norm', pos=(-0.5,0))
instr_B_pic = visual.ImageStim(win, units='norm', pos=(0.5,0))

#      During rating
instruction = visual.TextStim(win, units='norm', color='black', height=0.07, pos=(0,0.5), alignHoriz='center')
play_button = MyButton(win, -0.8,0.5,'play_start.png')
sound_label = visual.TextStim(win, units='norm', color='black', text=u'Play again', height=0.07, pos=(-0.8, 0.3), alignHoriz='center')
affiliation_scale = visual.RatingScale(win, showValue = False, showAccept = False, pos=[0,0], low = 1, high = 9, marker='circle', markerStart = 5, labels = ["1","2","3","4","5","6","7","8","9"], scale = u"Affiliatif: (1: pas du tout... 5: moyennement... 9: extrêmement)", stretch=2, textSize = 0.5, lineColor='Black', textColor='Black')
control_scale = visual.RatingScale(win, showValue = False, acceptText = u"Cliquez pour valider", acceptPreText = u"Cliquer sur l'échelle", showAccept = True, pos=[0,-0.4], low = 1, high = 9, marker='circle', markerStart = 5, labels =  ["1","2","3","4","5","6","7","8","9"], scale = u"Contrôlant: (1: pas du tout... 5: moyennement... 9: extrêmement)",  stretch=2, textSize = 0.5, lineColor='Black', textColor='Black')
affiliation_pic1 = visual.ImageStim(win, image=img_path+'affiliate1.png', units='norm', size = (0.3,0.2), pos=(-0.8,0))
affiliation_pic2 = visual.ImageStim(win, image=img_path+'affiliate2.png', units='norm', size = (0.3,0.2), pos=(0.8,0))
control_pic1 = visual.ImageStim(win, image=img_path+'control1.png', units='norm', size = (0.3,0.2), pos=(-0.8,-0.4))
control_pic2 = visual.ImageStim(win, image=img_path+'control2.png', units='norm', size = (0.3,0.2), pos=(0.8,-0.4))

#    Result and trial files
preference_result_file = generate_result_file(subject_number)
trial_files = generate_trial_files(subject_number)

#    Instructions
show_text_and_wait(file_name="intro.txt")  
show_text_and_pics_and_wait(file_name="affiliate.txt", pic1 = "affiliate1.png" , pic2 = "affiliate2.png")
show_text_and_pics_and_wait(file_name="control.txt", pic1 = "control1.png", pic2 = "control2.png")
show_text_and_pics_and_wait(file_name="mix.txt", pic1 = "mix1.png", pic2 = "mix2.png")
show_text_and_wait(file_name="intro_3.txt")

first_block = True
for trial_file in trial_files:
    trials = read_trials(trial_file)
    
    #    Music trials
    for trial in trials :

        audio_file = get_audio_file(trial)
        trial_sound = sound.Sound(value=sound_path+audio_file)
        
        #    Personalize with instruments name and picture
        instrument_A = trial[1]
        instrument_B = trial[2]
        trigger_instruction_text = u"Appuyez sur [ENTER] pour écouter l'extrait suivant. Faites attention au comportement du musicien de gauche ("+instrument_A+u"), vis à vis du musicien de droite ("+instrument_B+u")"
        trigger_instruction.text = trigger_instruction_text
        instr_A_pic.setImage(img_path+instrument_A+'-A.jpg')
        instr_B_pic.setImage(img_path+instrument_B+'-B.jpg')
        trial_instruction_text = u"Evaluez le comportement du musicien de gauche ("+instrument_A+u") vis à vis du musicien de droite ("+instrument_B+u") sur les deux échelles. Vous pouvez ré-écouter l'extrait si besoin."
        instruction.text = trial_instruction_text
        
        #    Play sounds
        update_play_gui()
        event.waitKeys()
        trial_sound.play()
        core.wait(2*trial_sound.getDuration()/3)
        end_trial = False
        response_start = time.getTime()
        affiliation_scale.reset() 
        control_scale.reset() 
        play_button.setImage('play_start.png')
        
        #    Rating scale
        while (not end_trial):
            update_preference_gui()
            while mouse.getPressed()[0] == 0:
                update_preference_gui()
            mouseX, mouseY = mouse.getPos()
            
            if mouse.isPressedIn(play_button.box) :
                trial_sound.play()
                play_button.setImage('play_on.png')
                while mouse.getPressed()[0] == 1:
                    core.wait(0.1) # prevent multiple plays   
                                
            if control_scale.noResponse == False:
                response_time = control_scale.getRT()         #    Record the response time
                affiliation = affiliation_scale.getRating()   #    Record the participant's result for affiliation
                control = control_scale.getRating()           #    Record the participant's result for control
                trial_sound.stop()
                end_trial = True
                win.flip()
                core.wait(0.5)
                        
        song = trial[0]
        cond = trial[3]
        manip = trial[4]
        write_preference_result(preference_result_file, subject_number,sex,age,date,song,cond,manip,audio_file,affiliation,control)

    #    2 minutes of pause
    if(first_block):
        show_text("pause2.txt")
        core.wait(60)
        show_text("pause1.txt")
        core.wait(60)
        show_text_and_wait("pause0.txt")
        first_block = False

#    End of experiment
show_text_and_wait("outro_FR.txt")

#    Close Python
win.close()
core.quit()
sys.exit()