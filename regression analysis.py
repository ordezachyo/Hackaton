from Subject import *

overlap_dict={'AG1': [1,'23:48:00'], 'CS7':[1,'21:29:00'], 'DS6':[1,'22:41:00'], 'EC0':[1,'23:54'], 'EG5':[1,'23:10:00'],
              'HS0':[1,'23:30:00'], 'JR9':[1,'22:48:00'], 'ME5':[0,'23:46:00'], 'MK2':[1,'22:32:00'], 'NS6':[0,'24:22:00'],'RP8':[1,'22:15:00'], 'TN8':[1,'24:54:00'], 'TR3':[1,'23:53:00'], 'TZ7':[1,'23:53:00']}
# Is there an overlap actigraph recording for the sleep lab recording?
sub_list = [fn.split('_')[0] for fn in os.listdir('CSVs')]

Subjects = []
for sub in sub_list:
    overlap = overlap_dict.get(sub)
    Subjects.append(Subject(sub,overlap))

