from Subject import *
from main_with_inputs import load_subject
import pytest

# This test checks the validity of all eeg scoring files (containing only--1, 0, 1, 2, 3, 4)
def test_eeg_scoring():
    Subjects, _ = load_subject()
    flag = False
    for sub in Subjects:
        txt = [fn for fn in os.listdir('watch_data/scoring_cntrl/') if fn.split('_')[0] == sub.name and fn.find('description') == -1][0]
        lab_sleep_score = pd.read_csv('watch_data/scoring_cntrl/' + txt)
        if (lab_sleep_score.values > 4).sum() > 0 or (lab_sleep_score.values<-1).sum() > 0:
            flag = True

    assert not flag

def test_action_4_csv():
    Subjects, _ = load_subject()
    flag = False
    for sub in Subjects():
        action_4_csv = sub.actigraph
        if 'SleSco' not in action_4_csv.columns:
            flag = True

    assert not flag








