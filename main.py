import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Subject import *
import matplotlib.pyplot as plt
import datetime


Subjects = []
overlap_dict={'AG1': [1,'23:48:00 07/25/2018'], 'CS7':[1,'21:29:00 10/23/2018'], 'DS6':[1,'22:41:00 08/19/2018'], 'EC0':[1,'23:54:00 08/28/2018'], 'EG5':[1,'23:10:00 03/04/2018'], 'HS0':[1,'23:30:00 07/17/2018'], 'JR9':[1,'22:48:00 02/18/2018'], 'ME5':[0,'23:46:00 04/24/2018'], 'MK2':[1,'22:32:00 11/19/2018'], 'NS6':[0,'00:22:00 03/19/2018'],'RP8':[1,'22:15:00 02/23/2018'], 'TN8':[1,'00:54:00 01/16/2018'], 'TR3':[1,'23:53:00 10/14/2018'], 'TZ7':[1,'23:53:00 04/10/2018']}
# Is there an overlap actigraph recording for the sleep lab recording?
sub_list = [fn.split('_')[0] for fn in os.listdir('CSVs')]

date_format_string = "%H:%M:%S %m/%d/%Y"

for sub in sub_list:
    overlap = (overlap_dict.get(sub))[0]
    EEG_start_time = datetime.datetime.strptime((overlap_dict.get(sub))[1], date_format_string)
    Subjects.append(Subject(sub,overlap, EEG_start_time))


for sub in Subjects:
    sub.plot_sleep_scores()
    plt.show()
