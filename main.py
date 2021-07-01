import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Subject import *
import matplotlib.pyplot as plt


Subjects = []
overlap_dict={'AG1': 1, 'CS7':1, 'DS6':1, 'EC0':1, 'EG5':1, 'HS0':1, 'JR9':1, 'ME5':0,
              'MK2':1, 'NS6':0,'RP8':1, 'TN8':1, 'TR3':1, 'TZ7':1} # Is there an overlap actigraph recording for the sleep lab recording?
sub_list = [fn.split('_')[0] for fn in os.listdir('CSVs')]

for sub in sub_list:
    overlap = overlap_dict.get(sub)
    Subjects.append(Subject(sub,overlap))


for sub in Subjects:
    sub.plot_sleep_scores()
    plt.show()