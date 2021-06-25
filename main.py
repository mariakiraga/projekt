# !/usr/bin/env python
# -*- coding: latin-1 -*-
import atexit
import codecs
import random
import csv
from os.path import join
import yaml
from psychopy import visual, event, gui, core
import atexit

@atexit.register
def reactions(keys):
    """
    Zbieranie informacji o przyci?ni?tym klawiszu.
    :param keys: klawisz
    :return: przyci?ni?ty klawisz
    """
    event.clearEvents()
    key = event.waitKeys(keyList=keys)
    return key[0]

def check_exit(key='Esc'): #sprawdzic czy dziala
    """
    Sprawdzic (w trakcie procedury) czy eksperymentator nie chce zakonczyc.
    """
    stop = event.getKeys(keyList=[key])
    if stop:
        raise Exception('Experiment finished by user! Esc pressed.')

def abort_with_error(err):
    """
    Wywolaj jesli wystapil blad.
    """
    raise Exception(err)

def read_text_from_file(file_name, insert=''):
    """
    Odczytywanie z pliku tekstowego i opcjonalnie dodawanie informacji generowanych dynamicznie.
    :param file_name: nazwa pliku do czytania
    :param insert:
    :return: wiadomosc
    """
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
    """
    Wy?wietlanie odczytanej wiadomo?ci. Z mo?liwo?ci? przej?cia dalej SPACJ?.
    :param win:
    :param file_name:
    :param insert:
    :return:
    """
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'])
    msg.draw()
    win.flip()
    event.waitKeys(keyList='space', timeStamped=clock)


def show_info_br(win, file_name, insert=''):
    """
    Wy?wietlanie odczytanej wiadomo?ci. Bez mo?liwo?ci przej?cia dalej SPACJ?.
    :param win:
    :param file_name:
    :param insert:
    :return:
    """
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'])
    msg.draw()
    win.flip()


@atexit.register
def save_data():
    """
    Zapisywanie zebranych danych do pliku csv.
    :return:
    """
    with open(join('results', datafile), "w", newline='') as df:
        write = csv.writer(df)
        write.writerows(RESULTS)


def run_trial(win, n_trials):
    """
    Opis jednego trialu.
    :param win:
    :param n_trials: liczba powtórze?
    :return:
    """
    global key, rt, con, corr, stim_type, previous_stim_type

    # losowanie bod?ca tak, ?e nie ma dwóch takich samych po sobie
    previous_stim_type = ""
    for i in range(n_trials):  # NIE DZIA?A!
        stim_type = random.choice(list(stim.keys()))
        while stim_type == previous_stim_type:
            stim_type = random.choice(list(stim.keys()))
            print(stim_type)
            previous_stim_type = stim_type
        # previous_stim_type = stim_type


   # fpunkt fiksacji
    fix.setAutoDraw(True)
    win.flip()
    core.wait(conf['FIX_CROSS_TIME'])  # wy?wietlanie samego punktu fiksacji

    # rozpocz?cie trialu
    event.clearEvents()
    win.callOnFlip(clock.reset)

    # prezentacja bod?ca
    stim[stim_type].setAutoDraw(True)
    win.flip()

    # czekanie na reakcj?
    '''
    key = "-"   #z góry key jest -, ale jak realcja to key zmienia si? w p,q
    key = reactions(conf['REACTION_KEYS'])

    rt = "-"   # z góry rt jest -, ale jezeli
    time_max = core.CountdownTimer(conf['TIME_MAX'])
    while time_max.getTime() > 0:
        rt = clock.getTime() '''

    r = reactions(conf['REACTION_KEYS'])
    while True:
        if r:  # przerwij, gdy zostanie wci?ni?ty klawisz
            rt = clock.getTime()
            break
    key = r

    stim[stim_type].setAutoDraw(False)
    fix.setAutoDraw(False)
    win.flip()

    # przerwa pomi?dzy trialami
    core.wait(conf['STIM_BREAK'])

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

# za?adowanie pliku config z parametrami
conf = yaml.load(open('config.yaml', encoding='utf-8'))

# ustawienia wizualne dla okna dialogowego
window = visual.Window(units="pix", color=conf['BACKGROUND_COLOR'], fullscr=False, size=(4000, 4000))
window.setMouseVisible(True)

# okno dialogowe
info = {'ID': '', 'PLEC': ['M', 'K'], 'WIEK': ''}
dlg = gui.DlgFromDict(info, title='Wpisz swoje dane :)')
if not dlg.OK:
    print("User exited")
    core.quit()

# Ogólne ID badanych z?o?one z informacji podanych w oknie dialogowym
ID = info['ID'] + info['PLEC'] + info['WIEK']

# nazwa pliku csv z wynikami badanego
datafile = '{}.csv'.format(ID)

# ustawienia okna na czas eksperymentu
window = visual.Window(units="pix", color=conf['BACKGROUND_COLOR'], fullscr=True, size=(1500, 1500))
window.setMouseVisible(False)

# bod?ce
fix = visual.TextStim(win=window, text="+", color=conf['FIX_CROSS_COLOR'], height=conf['FIX_CROSS_SIZE'])

stim = {"left_com":visual.TextStim(win=window, text="LEWO", height=conf['STIM_SIZE'],
                                     color=conf['STIM_COLOR'], pos=(-500.0, 0.0)),
            "left_incom":visual.TextStim(win=window, text="LEWO", height=conf['STIM_SIZE'],
                                       color=conf['STIM_COLOR'], pos=(500.0, 0.0)),
            "right_com":visual.TextStim(win=window, text="PRAWO", height=conf['STIM_SIZE'],
                                      color=conf['STIM_COLOR'], pos=(500.0, 0.0)),
            "right_incom":visual.TextStim(win=window, text="PRAWO", height=conf['STIM_SIZE'],
                                        color=conf['STIM_COLOR'], pos=(-500.0, 0.0))}

# informacje o eksperymencie, instrukcje
show_info(window, join('.', 'messages', 'instr.txt'))

# trening
show_info(window, join('.', 'messages', 'train_mess.txt'))

RESULTS = [["PART_ID", "TRIAL", "TRAINING", "CORRECT", "CONGRUENT", "LATENCY"]]

for block_no in range(conf['NO_BLOCK_TRAIN']):
    for a in range(conf['N_TRIALS_TRAIN']):
        trial_no = a
        trial_no += 1
        train = 1
        run_trial(window, conf['N_TRIALS_TRAIN'])

    window.flip()

# eksperyment
show_info(window, join('.', 'messages', 'exp_mess.txt'))

for block_no in range(conf['NO_BLOCK_EXP']):
    for i in range(conf['N_TRIALS_EXP']):
        trial_no = i
        train = 0
        run_trial(window, conf['N_TRIALS_EXP'])

    if block_no != conf['NO_BLOCK_EXP'] - 1:

        # PO 0 SEK OD WY?WIETLENIA BODZCA NIE MA REAKCJI NA KLIKNI?TE KLAWICZE
        event.waitKeys(maxWait=0)

        # przez TIME_FOR_REAST POKAZUJE SI? INFO BEZ SPACJI
        timer = core.CountdownTimer(conf['TIME_FOR_REAST'])
        while timer.getTime() > 0:
            show_info_br(window, join('.', 'messages', 'break_mess.txt'))
        show_info(window, join('.', 'messages', 'break_mess2.txt'))
        window.flip()

# zako?czenie
save_data()
show_info(window, join('.', 'messages', 'fin_mess.txt'))
window.close()
core.quit()