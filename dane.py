import codecs
import random
import csv
import atexit
from os.path import join
from statistics import mean

import yaml
from psychopy import visual, event, logging, gui, core

N_TRIALS_TRAIN = 1
N_TRAILS_EXP = 4
REACTION_KEYS = ['q', 'p']
RESULTS = [["TRIAL", "TRAINING", "TRIAL_TYPE", "REACTION", "CORRECT", "CONGRUENT","LATENCY"]]
#"ID","SEX","AGE",

def reactions(keys):
    event.clearEvents()
    key = event.waitKeys(keyList=keys)
    return key[0]

def read_text_from_file(file_name, insert=''):
    msg = list()
    with codecs.open(file_name, encoding='utf-8', mode='r') as data_file:
        for line in data_file:
            if not line.startswith('#'):  # if not commented line
                if line.startswith('<--insert-->'):
                    if insert:
                        msg.append(insert)
                else:
                    msg.append(line)
    return ''.join(msg)

def show_info(win, file_name, insert=''):
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color='black', text=msg,
                          height=20)
    msg.draw()
    win.flip()
    key = event.waitKeys(keyList=[chr(27), 'space'])
   # if key == [chr(27)]:
   #     abort_with_error(
    #        'Experiment finished by user on info screen! Esc pressed.')
    win.flip()


def part_of_experiment(n_trials, train, fix, time):
    for i in range(n_trials):
        stim_type = random.choice(list(stim.keys()))

        #fix point
        fix.setAutoDraw(True)
        window.flip()
        core.wait(1)

        window.callOnFlip(clock.reset)
        stim[stim_type].setAutoDraw(True)
        window.flip()
        key = reactions(REACTION_KEYS)

        stim[stim_type].setAutoDraw(False)
        fix.setAutoDraw(False)
        window.flip()
        core.wait(time)

        rt = clock.getTime()
        con = stim_type == key

        for stim_type in ["left_com", "left_incom"]:
            corr = 1
            print(corr)


        RESULTS.append([i+1, train, corr, con, rt])


window = visual.Window(units="pix", color="gray", fullscr=False, size=(1500, 1500))
window.setMouseVisible(False)

clock = core.Clock()

stim = {"left_com": visual.TextStim(win=window, text="LEWO", color="red", pos=(-500.0, 0.0), height=80),
        "left_incom": visual.TextStim(win=window, text="LEWO", color="red", pos=(500.0,0.0), height=80),
        "right_com": visual.TextStim(win=window, text="PRAWO", color="red", pos=(500.0,0.0), height=80),
        "right_incom": visual.TextStim(win=window, text="PRAWO", color="red", pos=(-500.0, 0.0), height=80)}

fix = visual.TextStim(win=window, text="+", color="black", height=60)

inst1 = visual.TextStim(win=window, text="instrukcja", color="white", height=40)
inst2 = visual.TextStim(win=window, text="teraz eksperyment", color="white", height=40)
inst_end = visual.TextStim(win=window, text="koniec", color="white", height=40)


# TRAINING
show_info(window, join('.', 'messages', 'train_mess.txt'))
part_of_experiment(N_TRIALS_TRAIN, train=True, fix=fix, time=1)

# EXPERIMENT
show_info(window, join('.', 'messages', 'exp_mess.txt'))
part_of_experiment(N_TRAILS_EXP, train=False, fix=fix, time=1)

# THE END
show_info(window, join('.', 'messages', 'fin_mess.txt'))

with open("result.csv", "w", newline='') as f:
    write = csv.writer(f)
    write.writerows(RESULTS)





