import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
sep = os.sep
sub_list = [fn for fn in os.listdir('CSVs')]
for sub in sub_list:
    csv = pd.read_csv('CSVs'+sep+sub)
    date, time = list(csv['Date'].values), list(csv['Time'].values)

    for i in range(len(time)):
        t = time[i]
        d = date[i]
        time[i] = int(t[:t.find(':')])
        date[i] = int(d.split('/')[1])

    date_ar = np.array(date)
    time_ar = np.array(time)

    rel = np.where((time_ar <= 10) | (time_ar >= 18))[0]
    rel_hours = csv.loc[list(rel), :]

    nights = list(np.unique(date_ar))[1:]
    num_nights = len(pd.unique(rel_hours.Date)) - 1


    date, time = list(rel_hours['Date'].values), list(rel_hours['Time'].values)
    date_d = []
    format_string = "%m/%d/%Y %H:%M:%S"
    for d, t in zip(date, time):
        date_d.append(datetime.datetime.strptime(f'{d} {t}', format_string))
    base_ind = 0
    end_count = 0
    start_count = 0
    end_inds = []
    start_inds = []
    for i, date in enumerate(date_d):
        try:
            if (date.hour == 18 and date.day == nights[start_count] and date.minute == 0):
                start_inds.append(i)
                start_count += 1
        except IndexError:
            pass
        try:
            if (date.hour==10 and date.day == nights[end_count] and date.minute == 0):
                end_inds.append(i)
                end_count+=1
        except IndexError:
            pass
        print('')

    dfs = []
    start_inds.insert(0, 0)
    end_inds.insert(2, len(date_d))
    start_ind = 0
    count = 0
    for i, j in zip(start_inds, end_inds):
        dfs.append(rel_hours.iloc[i:j])
    print('')

    for df in dfs:
        sleep_start, sleep_end = np.where(df.SleSco)[0][0], np.where(df.SleSco)[0][-1]
        df = df.iloc[sleep_start:sleep_end+1]


