import pandas as pd
import os
from yasa import sleep_statistics
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Subject():


    def __init__(self,name,overlap): #Create a subject object. name ('XX4') and path

        self.name = name
        self.overlap = overlap
        self.lab_sleep_score = pd.read_csv('watch_data/scoring_cntrl/'+name+'_hypnoWholeFile_revised.txt') # sleep score from the lab experiment
        self.st_lab = 1 # Hypnograph sample freq (HZ)
        self.st_watch = 1/60
        for acti_csv in os.listdir('CSVs'): # Locate data imported from the watch
            if acti_csv[0:name.__len__()] == self.name:
                self.acti_path = acti_csv # save the path as an attribute

        self.actigraph = pd.read_csv('CSVs/'+ self.acti_path) # load watch data
        self.actigraph = self.actigraph[['Date','Time','SleSco']] # keep only the relevent fields

    def plot_sleep_scores(self):
        lab_sleep_score_flat = self.lab_sleep_score.replace([2, 3, 4, -1], 1)
        lab_sleep_score_flat = pd.DataFrame.to_numpy(lab_sleep_score_flat)
        lab_sleep_score_flat = lab_sleep_score_flat.squeeze()
        self.lab_sleep_score_flat = lab_sleep_score_flat
        self.num_night_watch = 2
        #-------------------------------------------------------

        param = ['SE','WASO','SME','TST','SPT']

        self.stat_lab = sleep_statistics(self.lab_sleep_score_flat, self.st_lab)
        # df_plot = pd.DataFrame.from_dict(self.stat_lab, orient='index')
        # df_plot= df_plot.loc[param, :]
        for k, v in self.stat_lab.items():
            self.stat_lab[k] = round(v, 2)
        # Calculate statistics for watch nights FOR NOW USE THE DUMMY DATA

        watch_nights = [self.actigraph,self.actigraph]
        l = []

        for night in range(0,self.num_night_watch):
            l.append(sleep_statistics(watch_nights[night]['SleSco'] , self.st_watch))



        #----------------------Figure Time-------------------------------

        fig, ax = plt.subplots(self.num_night_watch+1,figsize=(10,10))
        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        fig.suptitle(f'Subject {self.name}')
        ax[0].plot(lab_sleep_score_flat)
        ax[0].set_title('In The Lab')

        ax[0].legend([extra, extra, extra,extra,extra], (f"SE={self.stat_lab['SE']}", f"WASO={self.stat_lab['WASO']}",f'SME={self.stat_lab["SME"]}', f"TST={self.stat_lab['TST']}",f"SPT={self.stat_lab['SPT']}"), loc=1)




        for night in range (1,self.num_night_watch+1):
          ax[night].plot(self.lab_sleep_score) #TO BE CHANGED TO ACTIGRAPH
          ax[night].set_title(f'{night}st Night (Watch)')






