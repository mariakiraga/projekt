from psychopy import visual, core, event
import random
import csv

N_TRIALS_TRAIN = 1
N_TRAILS_EXP = 4
REACTION_KEYS = ['q', 'p']
RESULTS = [["TRIAL", "TRAINING", "TRIAL_TYPE", "REACTION", "CORRECT", "CONGRUENT","LATENCY"]]
#"ID","SEX","AGE",

def reactions(keys):
    event.clearEvents()
    key = event.waitKeys(keyList=keys)
    return key[0]


def show_text(win, info, wait_key=["space"]):
    info.draw()
    win.flip()
    reactions(wait_key)


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
show_text(win=window, info=inst1)
part_of_experiment(N_TRIALS_TRAIN, train=True, fix=fix, time=1)

# EXPERIMENT
show_text(win=window, info=inst2)
part_of_experiment(N_TRAILS_EXP, train=False, fix=fix, time=1)

# THE END
show_text(win=window, info=inst_end)

with open("result.csv", "w", newline='') as f:
    write = csv.writer(f)
    write.writerows(RESULTS)





