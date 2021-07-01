from Subject import *
import matplotlib.pyplot as plt
from main_with_inputs import load_subject

def get_all_night_stats(Subjects, param):
    pre = ['1st_', '2nd_', '3rd_']
    # A list of all nights with watch features CSVs
    # The overlap night features csv
    night_list = [pd.DataFrame(columns=[pre[0] + fn for fn in param]),
                  pd.DataFrame(columns=[pre[1] + fn for fn in param]),
                  pd.DataFrame(columns=[pre[2] + fn for fn in param])]
    overlap = pd.DataFrame(columns=param)

    for i, sub in enumerate(Subjects):
        nights = sub.extract_night()
        if sub.overlap:
            overlap_night = nights.pop()
        else:
            overlap_night = sub.lab_sleep_score

        for j in range(len(nights)):
            night = nights[j]
            stats = sleep_statistics(night['SleSco'], sub.st_watch)
            for par in param:
                night_list[j].at[i, pre[j] + par] = stats.get(par)

        stats = sleep_statistics(overlap_night['SleSco'], sub.st_watch) if sub.overlap else sleep_statistics(
            overlap_night, sub.st_lab)

        for par in param:
            overlap.at[i, par] = stats.get(par)

    return night_list, overlap