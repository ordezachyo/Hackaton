import pandas as pd
import os
from yasa import sleep_statistics
import matplotlib.pyplot as plt

class Subject():


    def __init__(self,name,overlap): #Create a subject object. name ('XX4') and path
        self.overlap = overlap
        self.name = name
        self.lab_sleep_score = pd.read_csv('watch_data/scoring_cntrl/'+name+'_hypnoWholeFile_revised.txt') # sleep score from the lab experiment
        for acti_csv in os.listdir('CSVs'): # Locate data imported from the watch
            if acti_csv[0:name.__len__()] == self.name:
                self.acti_path = acti_csv # save the path as an attribute

        self.actigraph = pd.read_csv('CSVs/'+ self.acti_path) # load watch data
        self.actigraph = self.actigraph[['Date','Time','SleSco']] # keep only the relevent fields

    def plot_sleep_scores(self):
        self.lab_sleep_score
        lab_sleep_score_flat = self.lab_sleep_score.replace([2, 3, 4, -1], 1)
        lab_sleep_score_flat = pd.DataFrame.to_numpy(lab_sleep_score_flat)
        lab_sleep_score_flat = lab_sleep_score_flat.squeeze()

        fig, ax = plt.subplots(3,figsize=(10,10))

        ax[1].plot(self.lab_sleep_score)
        ax[2].plot(lab_sleep_score_flat)





