import pandas as pd
import os
import datetime
from yasa import sleep_statistics
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
class Subject(): # Object represent a single subject in the experiment

    def __init__(self,name,overlap): #Create a subject object- name: str, overlap: binary ('XX4')

        self.name = name
        self.overlap = overlap # does data from the watch overlaps with data from the lab)
        self.lab_sleep_score = pd.read_csv('watch_data/scoring_cntrl/'+name+'_hypnoWholeFile_revised.txt') # sleep score from the lab experiment
        self.st_lab = 1 # Hypnograph sample freq (HZ)
        self.st_watch = 1/60 # Hypnograph sample freq (HZ)

        for acti_csv in os.listdir('CSVs'):  # Locate data imported from the watch
            if acti_csv[0:name.__len__()] == self.name:
                self.acti_path = acti_csv  # save the path as an attribute

        self.actigraph = pd.read_csv('CSVs/' + self.acti_path)  # load watch data
        self.actigraph = self.actigraph[['Date', 'Time', 'SleSco']]  # keep only the relevent fields

        self.nights = self.extract_night()



    def plot_sleep_scores(self): # This function calculate statistics for both lab and watch data, then plots it nicely
        lab_sleep_score_flat = self.lab_sleep_score.replace([2, 3, 4, -1], 1)
        lab_sleep_score_flat = pd.DataFrame.to_numpy(lab_sleep_score_flat)
        lab_sleep_score_flat = lab_sleep_score_flat.squeeze()
        self.lab_sleep_score_flat = lab_sleep_score_flat

        #-------------------------------------------------------

        param = ['SE','WASO','SME','TST','SPT'] # staistic parameters to keep

        self.stat_lab = sleep_statistics(self.lab_sleep_score_flat, self.st_lab)
        for k, v in self.stat_lab.items(): # Round all floats
            self.stat_lab[k] = round(v, 2)
        # Calculate statistics for watch nights FOR NOW USE THE DUMMY DATA
        self.num_night_watch = len(self.nights)
        self.stat_watch = [] # list of dicts - each dict represent the statistics of a single watch night

        for night in range(0,self.num_night_watch): # for each watch night
            self.stat_watch.append(sleep_statistics(self.nights[night]['SleSco'] , self.st_watch)) # cal statistics

        for d in self.stat_watch: # Round all floats
            for k, v in d.items():
                d[k] = round(v, 2)



        #----------------------Figure Time-------------------------------

        fig, ax = plt.subplots(self.num_night_watch+1,figsize=(10,10))
        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        fig.suptitle(f'Subject {self.name}')
        ax[0].plot(lab_sleep_score_flat)
        ax[0].set_title('EEG binary scoring')

        ax[0].legend([extra, extra, extra,extra,extra], (f"SE={self.stat_lab['SE']}", f"WASO={self.stat_lab['WASO']}",f'SME={self.stat_lab["SME"]}', f"TST={self.stat_lab['TST']}",f"SPT={self.stat_lab['SPT']}"), loc=1)


        suf = ['st', 'nd', 'rd', 'th']

        for night in range (1,len(self.nights)+1):
          ax[night].plot(self.nights[night-1]['SleSco'].values) #TO BE CHANGED TO ACTIGRAPH
          ax[night].legend([extra, extra, extra, extra, extra], (
          f"SE={self.stat_watch[night-1]['SE']}", f"WASO={self.stat_watch[night-1]['WASO']}", f'SME={self.stat_watch[night-1]["SME"]}',
          f"TST={self.stat_watch[night-1]['TST']}", f"SPT={self.stat_watch[night-1]['SPT']}"), loc=1)

          ax[night].set_title(f'{night}{suf[night-1]} Night (Watch)')

    def time_date_ar(self, date, time):
        for i in range(len(time)):
            t = time[i]
            d = date[i]
            time[i] = int(t[:t.find(':')])
            date[i] = int(d.split('/')[1])

        date_ar = np.array(date)
        time_ar = np.array(time)

        return date_ar, time_ar


    def extract_night(self):
        date, time = list(self.actigraph['Date'].values), list(self.actigraph['Time'].values)

        date_ar, time_ar = self.time_date_ar(date, time)


        rel = np.where((time_ar <= 10) | (time_ar >= 19))[0]
        rel_hours = self.actigraph.loc[list(rel), :]

        nights = list(np.unique(date_ar))[1:]
        date, time = list(rel_hours['Date'].values), list(rel_hours['Time'].values)
        date_d = []
        format_string = "%m/%d/%Y %H:%M:%S"
        for d, t in zip(date, time):
            date_d.append(datetime.datetime.strptime(f'{d} {t}', format_string))

        end_count = 0
        start_count = 0
        end_inds = []
        start_inds = []

        for i, date in enumerate(date_d):
            try:
                if (date.hour == 19 and date.day == nights[start_count] and date.minute == 0):
                    start_inds.append(i)
                    start_count += 1
            except IndexError:
                pass
            try:
                if (date.hour == 10 and date.day == nights[end_count] and date.minute == 0):
                    end_inds.append(i)
                    end_count += 1
            except IndexError:
                pass

        dfs = []
        if len(nights)>1:
            start_inds.insert(0, 0)
            last_ind = len(nights)
            end_inds.insert(last_ind-1, len(date_d))
        else:
            pass

        for i, j in zip(start_inds, end_inds):
            dfs.append(rel_hours.iloc[i:j])

        for i, df in enumerate(dfs):
            sleep_start, sleep_end = np.where(df.SleSco)[0][0], np.where(df.SleSco)[0][-1]
            dfs[i] = df.iloc[sleep_start:sleep_end + 1]
        return dfs



