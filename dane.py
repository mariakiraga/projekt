import codecs
import random
import csv
from os.path import join

from psychopy import visual, event, gui, core

N_TRIALS_TRAIN = 1
N_TRAILS_EXP = 4
REACTION_KEYS = ['q', 'p']
RESULTS = [["ID", 'SEX', 'AGE', "TRIAL", "TRAINING", "CORRECT", "CONGRUENT", "LATENCY"]]


# RESULTS = [["ID", "TRIAL", "TRAINING", "CORRECT", "CONGRUENT","LATENCY"]]


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
                          height=40)
    msg.draw()
    win.flip()

def part_of_experiment(n_trials, train, fix, time):
    for i in range(n_trials):
        stim_type = random.choice(list(stim.keys()))

        # fix point
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

        RESULTS.append([id, sex, age, i + 1, train, corr, con, rt])
        # RESULTS.append([ID, i+1, train, corr, con, rt])


clock = core.Clock()

# VISUAL SETTINGS FOR DIALOG BOX
window = visual.Window(units="pix", color="gray", fullscr=False, size=(1500, 1500))
window.setMouseVisible(True)

# DIALOG BOX
info = {'ID': '', 'PLEC': ['M', 'K'], 'WIEK': ''}
dlg = gui.DlgFromDict(info, title='Wpisz swoje dane :)')
if not dlg.OK:
    print("User exited")
    core.quit()

# SAVING DATA TO CSV FILE
id = info['ID']
sex = info['PLEC']
age = info['WIEK']
# ID = info['ID'] + info['PLEC'] + info['WIEK']

datafile = '{}{}{}_data.csv'.format(info['ID'], info['PLEC'], info['WIEK'])
# datafile = 'ID.csv'

def save_data():
    with open(join('results', datafile), "w", newline='') as df:
        write = csv.writer(df)
        write.writerows(RESULTS)


# VISUAL SETTINGS FOR THE REST OF EXPERIMENT
window = visual.Window(units="pix", color="gray", fullscr=True, size=(1500, 1500))
window.setMouseVisible(False)

# STIMULI AND FIXATION POINT
stim = {"left_com": visual.TextStim(win=window, text="LEWO", color="red", pos=(-500.0, 0.0), height=80),
        "left_incom": visual.TextStim(win=window, text="LEWO", color="red", pos=(500.0, 0.0), height=80),
        "right_com": visual.TextStim(win=window, text="PRAWO", color="red", pos=(500.0, 0.0), height=80),
        "right_incom": visual.TextStim(win=window, text="PRAWO", color="red", pos=(-500.0, 0.0), height=80)}

fix = visual.TextStim(win=window, text="+", color="black", height=60)


# WELCOME MESSAGE WITH INSTRUCTIONS
show_info(window, join('.', 'messages', 'instr.txt'))

# TRAINING
show_info(window, join('.', 'messages', 'train_mess.txt'))
part_of_experiment(N_TRIALS_TRAIN, train=True, fix=fix, time=1)

# EXPERIMENT PT 1
show_info(window, join('.', 'messages', 'exp_mess.txt'))
part_of_experiment(N_TRAILS_EXP, train=False, fix=fix, time=1)

# BREAK
show_info(window, join('.', 'messages', 'break_mess.txt'))

# EXPERIMENT PT 2
part_of_experiment(N_TRAILS_EXP, train=False, fix=fix, time=1)

save_data()

# THE END
show_info(window, join('.', 'messages', 'fin_mess.txt'))
window.close()
