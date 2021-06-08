#!/usr/bin/env python
# -*- coding: latin-1 -*-
import atexit
import codecs
import csv
import random
from os.path import join
from statistics import mean

import yaml
from psychopy import visual, event, logging, gui, core

from misc.screen_misc import get_screen_res, get_frame_rate
from itertools import combinations_with_replacement, product


@atexit.register
def save_beh_results():
    """
    Save results of experiment. Decorated with @atexit in order to make sure, that intermediate
    results will be saved even if interpreter will broke.
    """
    with open(join('results', PART_ID + '_' + str(random.choice(range(100, 1000))) + '_beh.csv'), 'w', encoding='utf-8') as beh_file:
        beh_writer = csv.writer(beh_file)
        beh_writer.writerows(RESULTS)
    logging.flush()


def read_text_from_file(file_name, insert=''):
    """
    Method that read message from text file, and optionally add some
    dynamically generated info.
    :param file_name: Name of file to read
    :param insert:
    :return: message
    """
    if not isinstance(file_name, str):
        logging.error('Problem with file reading, filename must be a string')
        raise TypeError('file_name must be a string')
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


def check_exit(key=chr(27)): #sprawdzic czy dziala
    """
    Check (during procedure) if experimentator doesn't want to terminate.
    """
    stop = event.getKeys(keyList=[key])
    if stop:
        abort_with_error(
            'Experiment finished by user! Esc pressed.'.format(key))


def show_info(win, file_name, insert=''):
    """
    Clear way to show info message into screen.
    :param win:
    :return:
    """
    msg = read_text_from_file(file_name, insert=insert)
    msg = visual.TextStim(win, color='black', text=msg,
                          height=20, wrapWidth=SCREEN_RES['width'])
    msg.draw()
    win.flip()
    key = event.waitKeys(keyList=[chr(27), 'space', 'q', 'p'])
    if key == [chr(27)]:
        abort_with_error(
            'Experiment finished by user on info screen! Esc pressed.')
    win.flip()


def abort_with_error(err):
    """
    Call if an error occured.
    """
    logging.critical(err)
    raise Exception(err)


# GLOBALS

RESULTS = list()  # list in which data will be colected
RESULTS.append(['PART_ID', "TRIAL", "TRAINING", "TRIAL_TYPE", "REACTION", "CORRECT", "CONGRUENT","LATENCY"]  # ... Results header
# sex,age,id wszystkie poki co sa w part_id, ale czy to tak zostawiac czy nie

def main():
    global PART_ID  # PART_ID is used in case of error on @atexit, that's why it must be global

    # === Dialog popup ===
    info={'IDENTYFIKATOR': '', u'P\u0141EC': ['M', "K"], 'WIEK': '20'}
    dictDlg=gui.DlgFromDict(
        dictionary=info, title='Badanie efektu Simona, wpisz swoje imi?!')
    if not dictDlg.OK:
        abort_with_error('Info dialog terminated.')

    clock=core.Clock()
    # load config, all params are there
    conf=yaml.load(open('config.yaml', encoding='utf-8'))

    # === Scene init ===
    win=visual.Window(list(SCREEN_RES.values()), fullscr=False, monitor='testMonitor', units='pix',
                                       screen=0, color=conf['BACKGROUND_COLOR'])
    event.Mouse(visible=False, newPos=None, win=win)  # Make mouse invisible
    FRAME_RATE=get_frame_rate(win)

    # check if a detected frame rate is consistent with a frame rate for witch experiment was designed
    # important only if milisecond precision design is used
    #czy to potrzebne?? nie wiadomo, raczej nie

    if FRAME_RATE != conf['FRAME_RATE']:
        dlg=gui.Dlg(title="Critical error")
        dlg.addText(
            'Wrong no of frames detected: {}. Experiment terminated.'.format(FRAME_RATE))
        dlg.show()
        return None

    PART_ID=info['IDENTYFIKATOR'] + info[u'P\u0141EC'] + info['WIEK']
    logging.LogFile(join('results', PART_ID + '.log'),
                    level=logging.INFO)  # errors logging
    logging.info('FRAME RATE: {}'.format(FRAME_RATE)) # czy to znowu potrzebne? i to ni?ej
    logging.info('SCREEN RES: {}'.format(SCREEN_RES.values()))

    #Stimulus
    stim = {"left_com": visual.TextStim(win=window, text="LEWO", height=conf['STIM_SIZE'],
                                        color=conf['STIM_COLOR'] pos = conf['STIM_POS_L']),
    "left_incom": visual.TextStim(win=window, text="LEWO", height=conf['STIM_SIZE'],
                                  color=conf['STIM_COLOR']
    pos = conf['STIM_POS_R']),
    "right_com": visual.TextStim(win=window, text="PRAWO", height=conf['STIM_SIZE'],
                                 color=conf['STIM_COLOR']
    pos = conf['STIM_POS_R']),
    "right_incom": visual.TextStim(win=window, text="PRAWO", height=conf['STIM_SIZE'],
                                   color=conf['STIM_COLOR']
    pos = conf['STIM_POS_L'])}
    fix = visual.TextStim(win, text='+', height=60, color=conf['FIX_CROSS_COLOR'])

    # === Training ===

    show_info(win, join('.', 'messages', 'hello.txt'))

    trial_no += 1

    show_info(win, join('.', 'messages', 'before_training.txt'))
    csi_list=[conf['TRAINING_CSI']] * conf['NO_TRAINING_TRIALS'][1]
    for csi in csi_list:
        key_pressed, rt, ...=run_trial(win, conf, ...)
        corr=...# to raczej w funkcji trialu
        RESULTS.append([PART_ID, trial_no, 'training', ...])

        win.flip()

        trial_no += 1
        # === Experiment ===

    show_info(win, join('.', 'messages', 'before_experiment.txt'))

    for block_no in range(conf['NO_BLOCKS']):
        for _ in range(conf['Trials in block'])
            key_pressed, rt, ...=run_trial(win, conf, ...)
            RESULTS.append([PART_ID, block_no, trial_no, 'experiment', ...])
            trial_no += 1

        show_image(win, os.path.join('.', 'images', 'break.jpg'), # zamiast tego show info o przerwie + 30s do spacji funkcja
                   size=(SCREEN_RES['width'], SCREEN_RES['height']))

        # === Cleaning time ===
    save_beh_results()
    logging.flush()
    show_info(win, join('.', 'messages', 'end.txt'))
    win.close()
    core.quit()

def run_trial(win, ...):
    """
    Prepare and present single trial of procedure.
    Input (params) should consist all data need for presenting stimuli.
    If some stimulus (eg. text, label, button) will be presented across many trials.
    Should be prepared outside this function and passed for .draw() or .setAutoDraw().
    All behavioral data (reaction time, answer, etc. should be returned from this function)
    """

    # === Prepare trial-related stimulus ===
    # Randomise if needed
    #
    # Examples:
    #
    # que_pos = random.choice([-conf['STIM_SHIFT'], conf['STIM_SHIFT']])
    # stim.text = random.choice(conf['STIM_LETTERS'])
    #

    # === Start pre-trial  stuff (Fixation cross etc.)===

    # for _ in range(conf['FIX_CROSS_TIME']):
    #    fix_cross.draw()
    #    win.flip()

    # === Start trial ===
    # This part is time-crucial. All stims must be already prepared.
    # Only .draw() .flip() and reaction related stuff goes there.
    event.clearEvents()
    # make sure, that clock will be reset exactly when stimuli will be drawn
    win.callOnFlip(clock.reset)

    for _ in range(conf['STIM_TIME']):  # present stimuli
        reaction=event.getKeys(keyList=list(
            conf['REACTION_KEYS']), timeStamped=clock)
        if reaction:  # break if any button was pressed
            break
        stim.draw()
        win.flip()

    if not reaction:  # no reaction during stim time, allow to answer after that
        question_frame.draw()
        question_label.draw()
        win.flip()
        reaction=event.waitKeys(keyList=list(
            conf['REACTION_KEYS']), maxWait=conf['REACTION_TIME'], timeStamped=clock)
    # === Trial ended, prepare data for send  ===
    if reaction:
        key_pressed, rt=reaction[0]
    else:  # timeout
        key_pressed='no_key'
        rt=-1.0

    return key_pressed, rt  # return all data collected during trial

if __name__ == '__main__':
    PART_ID=''
    SCREEN_RES=get_screen_res()
    main()