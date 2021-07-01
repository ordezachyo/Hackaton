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
        txt = [fn for fn in os.listdir('watch_data/scoring_cntrl/') if fn.split('_')[0]==self.name][0]
        self.lab_sleep_score = pd.read_csv('watch_data/scoring_cntrl/'+txt) # sleep score from the lab experiment
        self.st_lab = 1 # Hypnograph sample freq (HZ)
        self.st_watch = 1/60 # Hypnograph sample freq (HZ)

        csv_name = [fn for fn in os.listdir('CSVs') if fn.split('_')[0] == self.name][0]
        csv = pd.read_csv('CSVs/' + csv_name)
        self.actigraph = csv[['Date', 'Time', 'SleSco']]  # keep only the relevent fields

        self.nights = self.extract_night()



    def plot_sleep_scores(self): # This function calculate statistics for both lab and watch data, then plots it nicely
        lab_sleep_score_flat = self.lab_sleep_score.replace([2, 3, 4], 1)
        lab_sleep_score_flat = lab_sleep_score_flat.replace(-1, np.nan)
        lab_sleep_score_flat = pd.DataFrame.to_numpy(lab_sleep_score_flat).squeeze()

        #-------------------------------------------------------

        # param = ['SE','WASO','SME','TST','SPT'] # staistic parameters to keep

        self.stat_lab = sleep_statistics(lab_sleep_score_flat, self.st_lab)
        for k, v in self.stat_lab.items(): # Round all floats
            self.stat_lab[k] = round(v, 2)
        # Calculate statistics for watch nights
        self.num_night_watch = len(self.nights)
        self.stat_watch = [] # list of dicts - each dict represent the statistics of a single watch night
        for night in range(0,self.num_night_watch): # for each watch night
            self.stat_watch.append(sleep_statistics(self.nights[night]['SleSco'], self.st_watch)) # cal statistics

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

          if self.overlap and night==len(self.nights):
              ax[night].set_title(f'{night}{suf[night - 1]} Overlap Night (Watch)')
          else:
              ax[night].set_title(f'{night}{suf[night-1]} Night (Watch)')

          plt.sca(ax[night])
          plt.xticks([0, int(len(self.nights[night-1])/2), len(self.nights[night-1])], [self.nights[night-1].iloc[0].Time[:-3], self.nights[night-1].iloc[int(len(self.nights[night-1])/2)].Time[:-3], self.nights[night-1].iloc[-1].Time[:-3]])
          # plt.setp(ax[night], xticks=[0, int(len(self.nights[night-1])/2), self.nights[night-1]], xlabels=[self.nights[night-1].iloc[0].Time, self.nights[night-1].iloc[int(len(self.nights[night-1])/2)].Time, self.nights[night-1].iloc[-1].Time])

        plt.setp(ax, yticks=[0, 1])
          # plt.setp(ax[1:], xticks=[0, 1])
        plt.show()

    def time_date_ar(self, date, time):
        '''
        This function calulates date and time arrays with only the day and hour
        :param date: (list) list of dates in a the dataframe
        :param time: (list) list of times in a the dataframe
        :return: 2 np arrays representing the date in day and time in hour
        '''

        # takes only the day and hour from each date and time
        for i in range(len(time)):
            t = time[i]
            d = date[i]
            time[i] = int(t[:t.find(':')])
            date[i] = int(d.split('/')[1])

        date_ar = np.array(date)
        time_ar = np.array(time)

        return date_ar, time_ar


    def extract_night(self):
        # Defines when the night starts
        night_start, night_end = 19, 10
        # Gets date and time in forms of array
        date, time = list(self.actigraph['Date'].values), list(self.actigraph['Time'].values)
        date_ar, time_ar = self.time_date_ar(date, time)
        # Takes only relevant hours according to night_start' and 'night_end'
        rel = np.where((time_ar <= night_end) | (time_ar >= night_start))[0]
        rel_hours = self.actigraph.loc[list(rel), :]

        # format date and time arrays to one datetime format to ease the calculations
        date, time = list(rel_hours['Date'].values), list(rel_hours['Time'].values)
        date_d = []
        format_string = "%m/%d/%Y %H:%M:%S"
        for d, t in zip(date, time):
            date_d.append(datetime.datetime.strptime(f'{d} {t}', format_string))


        # To store nights start and end indices
        end_count = 0
        start_count = 0
        end_inds = []
        start_inds = []
        #unique dates list
        nights = list(np.unique(date_ar))[1:]

        # extract indices of each night start and end according to the time and date
        for i, date in enumerate(date_d):
            # find first the start pf the second night and so on
            try:
                if (date.hour == night_start and date.day == nights[start_count] and date.minute == 0):
                    start_inds.append(i)
                    start_count += 1
            except IndexError:
                pass
            try:
            # # find the end of the first night and so on
                if (date.hour == night_end and date.day == nights[end_count] and date.minute == 0):
                    end_inds.append(i)
                    end_count += 1
            except IndexError:
                pass

        # inserts the beginning of the first night and the end of the last night to start and end arrays
        dfs = []
        start_inds.insert(0, 0)
        last_ind = len(nights) if len(nights) > 1 else 2
        end_inds.insert(last_ind-1, len(date_d))

        # Deals with only 1 night of measurement
        if len(nights)==1:
            start_inds = start_inds[:-1]
            end_inds = end_inds[:-1]

        # Creates a unique to dataframe for each on relevant hours
        for i, j in zip(start_inds, end_inds):
            dfs.append(rel_hours.iloc[i:j])

        # Trims 0 from the edges of each dataframe
        for i, df in enumerate(dfs):
            sleep_start, sleep_end = np.where(df.SleSco)[0][0], np.where(df.SleSco)[0][-1]
            dfs[i] = df.iloc[sleep_start:sleep_end + 1]

        return dfs 



