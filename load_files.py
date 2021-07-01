import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

def find_ones(csv):
    indices = []
    copy = csv.copy()
    nights = len(pd.unique(copy.Date))-1
    # ones_csv = copy[copy.SleSco == 1]
    drop = []

    date, time = list(copy['Date'].values), list(copy['Time'].values)

    for i in range(len(time)):
        t = time[i]
        d = date[i]
        time[i] = int(t[:t.find(':')])
        date[i] = int(d.split('/')[1])

        date_ar = np.array(date)
        time_ar = np.array(time)

        rel_ = np.where((time_ar < 10) | (time_ar > 18))


    start_ind = 0


    start_hour, end_hour = 18, 10




    start = 0
    nights_csv = []
    for n in range(nights):
        inds = time.index(str(end_hour))
        if n==0:
            nights_csv.append(copy.iloc[0:inds])

        else:

            start = inds
            time = time[inds:]

    flag = False
    for i, time in enumerate(copy['Time'].values):
        if time.find(':') != 1:
            hour = int(time[:2])
        else:
            hour = int(time[:1])
        if hour<18 and hour>10:
            drop.append(i)

    copy.drop(drop, axis=0, inplace=True)

    curr_date = copy.iloc[0].Date
    flag = False
    for i in range(len(copy)):
        time = copy.iloc[i].Time
        if time.find(':') != 1:
            hour = int(time[:2])
        else:
            hour = int(time[:1])

        slesco = copy.iloc[i].SleSco
        date = copy.iloc[i].Date

        if slesco == 1 and not flag:
            count = 0
            data_frame = pd.DataFrame(columns=copy.columns)
            flag = True
            curr_date_init = date
            data_frame.at[count, :] = copy.iloc[i]
            count+=1
            print('')


        print('')

    print('')


    nights = len(pd.unique(ones_csv['Date']))-1

    for un in pd.unique(pd.unique(ones_csv['Date'])):
        curr_pd = ones_csv[ones_csv['Date']==un]
        print('')
    for j in range(nights):
        curr_data_frame = pd.DataFrame(columns=ones_csv.columns)
        for i in range(len(ones_csv)):
            row = ones_csv.iloc[0]




        print('')


    print('')

sep = os.sep
ticks = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
sub_list = [fn for fn in os.listdir('CSVs')]
for sub in sub_list:
    csv = pd.read_csv('CSVs'+sep+sub)
    find_ones(csv)
    # plt.plot(csv.SleSco.values)
    # tick_list = []
    # for i in ticks:
    #     try:
    #         tick_list.append(csv.loc[i, 'Time'][:-3])
    #     except KeyError:
    #         pass
    # plt.xticks(np.arange(0, len(tick_list*500), 500), tick_list)
    # plt.show()


    print('')
