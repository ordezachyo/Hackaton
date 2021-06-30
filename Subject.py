import pandas as pd
import os
from yasa import sleep_statistics

class Subject():


    def __init__(self,name): #Create a subject object. name ('XX4') and path
        self.name = name
        self.lab_sleep_score = pd.read_csv('watch_data/scoring_cntrl/'+name+'_hypnoWholeFile_revised.txt')
        for acti_csv in os.listdir('CSVs'):
            if acti_csv[0:name.__len__()] == self.name:
                self.acti_path = acti_csv

        self.actigraph = pd.read_csv('CSVs/'+ self.acti_path)
        self.actigraph = self.actigraph[['Date','Time','SleSco']]




