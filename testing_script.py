from Subject import *
from main_with_inputs import load_subject
import pytest
import datetime

# This test checks the validity of all eeg scoring files (containing only--1, 0, 1, 2, 3, 4)
def test_eeg_scoring():
    Subjects, _ = load_subject()
    flag = False
    for sub in Subjects:
        txt = [fn for fn in os.listdir('watch_data/scoring_cntrl/') if fn.split('_')[0] == sub.name and fn.find('description') == -1][0]
        lab_sleep_score = pd.read_csv('watch_data/scoring_cntrl/' + txt)
        if (lab_sleep_score.values > 4).sum() > 0 or (lab_sleep_score.values<-1).sum() > 0:
            flag = True
            break

    assert not flag

# Check the validity of SleSco column exists and valid
def test_action_4_csv():
    Subjects, _ = load_subject()
    flag = False
    for sub in Subjects:
        action_4_csv = sub.actigraph
        if 'SleSco' not in action_4_csv.columns:
            flag = True
            break
        if not flag:
            if (action_4_csv['SleSco'].values > 1).sum()>0 or (action_4_csv['SleSco'].values < 0).sum()>0:
                flag = True
                break
    assert not flag

def test_Subject_class():
    date_format_string = "%H:%M:%S %m/%d/%Y"
    flag = False

    right_name, wrong_name, wrong_name_2 = 'ME5', 0, 'vv'
    right_overlap, wrong_overlap = 0, 2
    right_time, wrong_time = datetime.datetime.strptime('22:32:00 11/19/2018', date_format_string), '22:32:00 11/19/2018'
    wrong_inputs = [[right_name, right_overlap, wrong_time], [right_name, wrong_overlap, right_time], [wrong_name, right_overlap, right_time], [wrong_name_2, right_overlap, right_time]]
    right_inputs = ['ME5', right_overlap, right_time]
    # The Value error is supposed to be raised
    for inp in wrong_inputs:
        try:
           sub = Subject(*inp)
        except ValueError:
            flag = True
    # The value error is not supposed to be raised
    try:
        sub = Subject(*right_inputs)
    except ValueError:
        flag = False

    assert flag

def test_validity_of_over_lap_dict_input():
    Subjects, _ = load_subject()
    flag = False

    for sub in Subjects:
        overlap = sub.overlap
        eeg_time = sub.EEG_start_time

        if overlap not in [0, 1] or type(eeg_time) != datetime.datetime:
            flag = True
    assert not flag










