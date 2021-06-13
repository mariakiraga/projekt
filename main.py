import codecs
import random
import csv
from os.path import join

from psychopy import visual, event, gui, core

N_TRIALS_TRAIN = 1
N_TRAILS_EXP = 4
REACTION_KEYS = ['q', 'p']
RESULTS = [["PART_ID", "TRIAL", "TRAINING", "CORRECT", "CONGRUENT","LATENCY"]]


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
    win.flip()

def show_text_pop(win, info):
    info.draw()
    win.flip()
    core.wait(0.5)


def save_data():
    with open(join('results', datafile), "w", newline='') as df:
        write = csv.writer(df)
        write.writerows(RESULTS)


def part_of_experiment(n_trials, train, fix, time):
    previous_stim_type = ""
    for i in range(n_trials):
        stim_type = random.choice(list(stim.keys()))
        while stim_type == previous_stim_type:
            stim_type = random.choice(list(stim.keys()))
        previous_stim_type = stim_type

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

        #odpowiedz zwrotna w treningu
        if train == True:
            if stim_type == "left_com" and key == "q":
                show_text_pop(win=window, info=popr)
            elif stim_type == "left_incom" and key == "q":
                show_text_pop(win=window, info=popr)
            elif stim_type == "right_com" and key == "p":
                show_text_pop(win=window, info=popr)
            elif stim_type == "right_com" and key == "p":
                show_text_pop(win=window, info=popr)
            else:
                show_text_pop(win=window, info=niepopr)

        rt = clock.getTime()
        # corr = poprawność
        if stim_type == "left_com" and key == "q":
            corr = 1
        elif stim_type == "left_incom" and key == "q":
            corr = 1
        elif stim_type == "right_com" and key == "p":
            corr = 1
        elif stim_type == "right_com" and key == "p":
            corr = 1
        else:
            corr = 0

        # con = zgodnosc
        if stim_type == "left_com":
            con = 1
        elif stim_type == "right_com":
            con = 1
        elif stim_type == "left_incom":
            con = 0
        elif stim_type == "right_incom":
            con = 0


        RESULTS.append([i+1, train, corr, con, rt])




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

ID = info['ID'] + info['PLEC'] + info['WIEK']
datafile = 'ID.csv'

window = visual.Window(units="pix", color="gray", fullscr=True, size=(1500, 1500))
window.setMouseVisible(False)

stim = {"left_com": visual.TextStim(win=window, text="LEWO", color="red", pos=(-500.0, 0.0), height=80),
        "left_incom": visual.TextStim(win=window, text="LEWO", color="red", pos=(500.0,0.0), height=80),
        "right_com": visual.TextStim(win=window, text="PRAWO", color="red", pos=(500.0,0.0), height=80),
        "right_incom": visual.TextStim(win=window, text="PRAWO", color="red", pos=(-500.0, 0.0), height=80)}

fix = visual.TextStim(win=window, text="+", color="black", height=60)

inst1 = visual.TextStim(win=window, text="instrukcja", color="white", height=40)
inst2 = visual.TextStim(win=window, text="teraz eksperyment", color="white", height=40)
inst_end = visual.TextStim(win=window, text="koniec", color="white", height=40)
popr = visual.TextStim(win=window, text="Poprawnie :)", color="white", height=40)
niepopr = visual.TextStim(win=window, text="Niepoprawnie :(", color="white", height=40)

# TRAINING
show_info(window, join('.', 'messages', 'train_mess.txt'))
part_of_experiment(N_TRIALS_TRAIN, train=True, fix=fix, time=1)

# EXPERIMENT
show_info(window, join('.', 'messages', 'exp_mess.txt'))
part_of_experiment(N_TRAILS_EXP, train=False, fix=fix, time=1)

# THE END
save_data()
show_info(window, join('.', 'messages', 'fin_mess.txt'))
window.close()






