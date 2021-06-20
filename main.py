import codecs
import random
import csv
from os.path import join

import yaml
from psychopy import visual, event, gui, core


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
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'])
    msg.draw()
    win.flip()
    event.waitKeys(keyList='space', timeStamped=clock)


def show_info_br(win, file_name, insert=''):
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'])
    msg.draw()
    win.flip()


def save_data():
    with open(join('results', datafile), "w", newline='') as df:
        write = csv.writer(df)
        write.writerows(RESULTS)


def run_trial(win, n_trials):
    global key, rt, con, corr, stim_type

    # LOSOWANIE BODZCA TAK, ZE NIE MA DWOCH TAKICH SAMYCH PO SOBIE
    previous_stim_type = ""
    for i in range(n_trials):                           #NIE DZIAŁA!
        stim_type = random.choice(list(stim.keys()))
        while stim_type == previous_stim_type:
            stim_type = random.choice(list(stim.keys()))
            previous_stim_type = stim_type

        # fix point
    fix.setAutoDraw(True)
    win.flip()
    core.wait(conf['FIX_CROSS_TIME'])  # wyświetlanie samego punktu fiksacji

    # === Start trial ===
    event.clearEvents()
    win.callOnFlip(clock.reset)

#PREZENTACJA BODZCA
    stim[stim_type].setAutoDraw(True)
    win.flip()

#CZEKANIE NA REAKCJE
    '''
    key = "-"   #z góry key jest -, ale jak realcja to key zmienia się w p,q
    key = reactions(conf['REACTION_KEYS'])

    rt = "-"   # z góry rt jest -, ale jezeli
    time_max = core.CountdownTimer(conf['TIME_MAX'])
    while time_max.getTime() > 0:
        rt = clock.getTime() '''

    r = reactions(conf['REACTION_KEYS'])
    while True:
        if r:  # break if any button was pressed
            rt = clock.getTime()
            break
    key = r


    stim[stim_type].setAutoDraw(False)
    fix.setAutoDraw(False)
    win.flip()

    #PRZERWA POMIĘDZY TRIALAMI
    core.wait(conf['STIM_BREAK'])
    # core.wait(random.randrange((conf['STIM_BREAK'])))


    # corr = poprawnosc
    if (stim_type == "left_com" and key == "q") or (stim_type == "left_incom" and key == "q") or \
            ("right_com" == stim_type and key == "p") or (stim_type == "right_incom" and key == "p"):
        corr = 1
    elif (stim_type == "left_com" and key == "p") or (stim_type == "left_incom" and key == "p") or \
        (stim_type == "right_com" and key == "q") or (stim_type == "right_incom" and key == "q"):
        corr = 0
    else:
        corr = "-"

    # con = zgodnosc
    if stim_type == "left_com" or stim_type == "right_com":
        con = 1
    elif (stim_type == "left_incom") or stim_type == "right_incom":
        con = 0
    else:
        con = "-"

    RESULTS.append([ID, trial_no, train, corr, con, rt])


# main
clock = core.Clock()

# load config, all params are their
conf = yaml.load(open('config.yaml', encoding='utf-8'))

# VISUAL SETTINGS FOR DIALOG BOX
window = visual.Window(units="pix", color=conf['BACKGROUND_COLOR'], fullscr=False, size=(4000, 4000))
window.setMouseVisible(True)

# DIALOG BOX
info = {'ID': '', 'PLEC': ['M', 'K'], 'WIEK': ''}
dlg = gui.DlgFromDict(info, title='Wpisz swoje dane :)')
if not dlg.OK:
    print("User exited")
    core.quit()

ID = info['ID'] + info['PLEC'] + info['WIEK']
datafile = '{}.csv'.format(ID)

window = visual.Window(units="pix", color=conf['BACKGROUND_COLOR'], fullscr=True, size=(1500, 1500))
window.setMouseVisible(False)

# stymulusy
fix = visual.TextStim(win=window, text="+", color=conf['FIX_CROSS_COLOR'], height=conf['FIX_CROSS_SIZE'])

stim = dict(left_com=visual.TextStim(win=window, text="LEWO", height=conf['STIM_SIZE'],
                                     color=conf['STIM_COLOR'], pos=(-500.0, 0.0)),
            left_incom=visual.TextStim(win=window, text="LEWO", height=conf['STIM_SIZE'],
                                       color=conf['STIM_COLOR'], pos=(500.0, 0.0)),
            right_com=visual.TextStim(win=window, text="PRAWO", height=conf['STIM_SIZE'],
                                      color=conf['STIM_COLOR'], pos=(500.0, 0.0)),
            right_incom=visual.TextStim(win=window, text="PRAWO", height=conf['STIM_SIZE'],
                                        color=conf['STIM_COLOR'], pos=(-500.0, 0.0)))

show_info(window, join('.', 'messages', 'instr.txt'))
# training
show_info(window, join('.', 'messages', 'train_mess.txt'))

RESULTS = [["PART_ID", "TRIAL", "TRAINING", "CORRECT", "CONGRUENT", "LATENCY"]]

for block_no in range(conf['NO_BLOCK_TRAIN']):
    for a in range(conf['N_TRIALS_TRAIN']):
        trial_no = a
        trial_no += 1
        train = 1
        run_trial(window, conf['N_TRIALS_TRAIN'])
        # corr, con, rt = run_trial(window, conf['N_TRIALS_TRAIN'])
        # RESULTS.append([ID, trial_no, train, corr, con, rt])  # 1-trening

    window.flip()

'''# === Experiment part 1 ==='''

show_info(window, join('.', 'messages', 'exp_mess.txt'))

for block_no in range(conf['NO_BLOCK_EXP']):
    for i in range(conf['N_TRIALS_EXP']):
        trial_no = i
        train = 0
        run_trial(window, conf['N_TRIALS_EXP'])
        # corr, con, rt = run_trial(window, conf['N_TRIALS_EXP'])
        # RESULTS.append([ID, trial_no, 0, corr, con, rt]) #0 - eksperyment
    if block_no != conf['NO_BLOCK_EXP'] - 1:

        #PO 0 SEK OD WYŚWIETLENIA BODZCA NIE MA REAKCJI NA KLIKNIĘTE KLAWICZE
        event.waitKeys(maxWait=0)

        #przez TIME_FOR_REAST POKAZUJE SIĘ INFO BEZ SPACJI
        timer = core.CountdownTimer(conf['TIME_FOR_REAST'])
        while timer.getTime() > 0:
            show_info_br(window, join('.', 'messages', 'break_mess.txt'))
        show_info(window, join('.', 'messages', 'break_mess2.txt'))
        window.flip()

# THE END
save_data()
show_info(window, join('.', 'messages', 'fin_mess.txt'))
window.close()
core.quit()

# co z errorem?
