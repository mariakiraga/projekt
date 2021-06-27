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
    Wyswietlanie odczytanej wiadomosci. Z mozliwoscia przejscia dalej SPACJA.
    :param win:
    :param file_name:
    :param insert:
    :return:
    """
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'])
    msg.draw()
    win.flip()
    key = event.waitKeys(keyList=['g', 'space'])
    if key == ['g']:
        win.close()
        core.quit()
    win.flip()


def show_info_br(win, file_name, insert=''):
    """
    Wyswietlanie odczytanej wiadomosci. Bez mozliwosci przejscia dalej SPACJA.
    :param win:
    :param file_name:
    :param insert:
    :return:
    """
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color=conf['TEXT_COLOR'], text=msg, height=conf['TEXT_SIZE'])
    msg.draw()
    win.flip()
    key = event.getKeys(keyList=['g'])
    if key == ['g']:
        win.close()
        core.quit()


def save_data():
    """
    Zapisywanie zebranych danych do pliku csv.
    :return:
    """
    with open(join('results', datafile), "w", newline='') as df:
        write = csv.writer(df)
        write.writerows(RESULTS)


def run_trial(win,):
    """
    Opis jednego trialu.
    :param win:
    :param n_trials: liczba powtórzen
    :return:
    """
    global key, rt, con, corr, stim_type, prev_stim

#losowanie bodzca tak, ze nie ma dwóch takich samych po sobie
    stim_type = random.choice(list(stim.keys()))
    while stim_type == prev_stim:
        stim_type = random.choice(list(stim.keys()))
    prev_stim = stim_type

   # punkt fiksacji
    fix.setAutoDraw(True)
    win.flip()
    core.wait(conf['FIX_CROSS_TIME'])  # wyswietlanie samego punktu fiksacji

    # rozpoczecie trialu
    event.clearEvents()
    win.callOnFlip(clock.reset)

    # prezentacja bodzca
    stim[stim_type].setAutoDraw(True)
    win.flip()

    # czekanie na reakcje
    while clock.getTime() <= conf['TIME_MAX']:
        k = event.getKeys(conf['REACTION_KEYS'])
        if k == ['q'] or k == ['p']:
            rt = clock.getTime()
            win.flip()
            break
        if k == ['g']:
            win.close()
            core.quit()
        win.flip()

    key = k
    print(key)
    if clock.getTime() > conf['TIME_MAX']:
        rt = '-'
        win.flip()


    stim[stim_type].setAutoDraw(False)
    fix.setAutoDraw(False)
    win.flip()

    # przerwa pomiedzy trialami
    core.wait(conf['STIM_BREAK'])

    # corr = poprawnosc
    if (stim_type == "left_com" and key == ['q']) or (stim_type == "left_incom" and key == ['q']) or \
            ("right_com" == stim_type and key == ['p']) or (stim_type == "right_incom" and key == ['p']):
        corr = 1
    elif (stim_type == "left_com" and key == ['p']) or (stim_type == "left_incom" and key == ['p']) or \
        (stim_type == "right_com" and key == ['q']) or (stim_type == "right_incom" and key == ['q']):
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

# zaladowanie pliku config z parametrami
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

# Ogólne ID badanych zlozone z informacji podanych w oknie dialogowym
ID = info['ID'] + info['PLEC'] + info['WIEK']

# nazwa pliku csv z wynikami badanego
datafile = '{}.csv'.format(ID)

# ustawienia okna na czas eksperymentu
window = visual.Window(units="pix", color=conf['BACKGROUND_COLOR'], fullscr=True, size=(1500, 1500))
window.setMouseVisible(False)

# bodzce
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
show_info(window, join('.', 'messages', 'instr2.txt'))

# trening
show_info(window, join('.', 'messages', 'train_mess.txt'))

RESULTS = [["PART_ID", "TRIAL", "TRAINING", "CORRECT", "CONGRUENT", "LATENCY"]]

for block_no in range(conf['NO_BLOCK_TRAIN']):
    for a in range(conf['N_TRIALS_TRAIN']):
        if a == 0:
            prev_stim = '0'
        print(prev_stim)
        trial_no = a
        trial_no += 1
        train = 1
        run_trial(window)

    window.flip()

# eksperyment
show_info(window, join('.', 'messages', 'exp_mess.txt'))

for block_no in range(conf['NO_BLOCK_EXP']):
    for i in range(conf['N_TRIALS_EXP']):
        if i == 0:
            prev_stim = '0'
        print(prev_stim)
        trial_no = i
        trial_no += 1
        train = 0
        run_trial(window)

    if block_no != conf['NO_BLOCK_EXP'] - 1:

        # po 0 sek od wyswietlenia bodzca nie ma reakcji na klikniecie klawisze
        event.waitKeys(maxWait=0)

        # przez TIME_FOR_REAST pakazuje sie info bez spacji
        timer = core.CountdownTimer(conf['TIME_FOR_REAST'])
        while timer.getTime() > 0:
            show_info_br(window, join('.', 'messages', 'break_mess.txt'))
        show_info(window, join('.', 'messages', 'break_mess2.txt'))
        window.flip()

# zakonczenie
save_data()
show_info(window, join('.', 'messages', 'fin_mess.txt'))
window.close()
core.quit()