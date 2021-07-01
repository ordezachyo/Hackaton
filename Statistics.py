
def get_all_night_stats(Subjects, param = ['SE','WASO','SME','TST','SPT']):
    from yasa import sleep_statistics
    import pandas as pd
    pre = ['1st_', '2nd_', '3rd_', 'Watch_']
    # A list of all nights with watch features CSVs
    # The overlap night features csv
    night_list = [pd.DataFrame(columns=[pre[0] + fn for fn in param]+['Name']),
                  pd.DataFrame(columns=[pre[1] + fn for fn in param]+['Name']),
                  pd.DataFrame(columns=[pre[2] + fn for fn in param]+['Name'])]

    lab_eeg = pd.DataFrame(columns=param)
    overlap_night = pd.DataFrame(columns=[pre[2] + fn for fn in param]+['Name'])

    nights_length = [sub.nights for sub in Subjects]


    for i, sub in enumerate(Subjects):
        nights = sub.nights
        if sub.overlap:
            o_night = nights.pop()
            o_stats = sleep_statistics(o_night['SleSco'], sub.st_watch)

        for j in range(len(nights)):
            night = nights[j]
            stats = sleep_statistics(night['SleSco'], sub.st_watch)
            for par in param:
                night_list[j].at[i, pre[j] + par] = stats.get(par)
                if sub.overlap:
                    overlap_night.at[i, pre[-1]+par] = o_stats.get(par)
                    overlap_night.at[i, 'Name'] = sub.name
            night_list[j].at[i, 'Name'] = sub.name

        lab_stats = sleep_statistics(sub.lab_sleep_score, sub.st_lab)

        for par in param:
            lab_eeg.at[i, par] = lab_stats.get(par)
            lab_eeg.at[i, 'Name'] = sub.name

    for night in night_list:
        night.set_index('Name', inplace=True)
    lab_eeg.set_index('Name', inplace=True)
    overlap_night.set_index('Name', inplace=True)

    return night_list, lab_eeg, overlap_night