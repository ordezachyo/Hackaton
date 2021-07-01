from Subject import *
import matplotlib.pyplot as plt

def get_regression_analysis(predictors, to_predict):
    to_p


overlap_dict={'AG1': [1,'23:48:00'], 'CS7':[1,'21:29:00'], 'DS6':[1,'22:41:00'], 'EC0':[1,'23:54'], 'EG5':[1,'23:10:00'],
              'HS0':[1,'23:30:00'], 'JR9':[1,'22:48:00'], 'ME5':[0,'23:46:00'], 'MK2':[1,'22:32:00'], 'NS6':[0,'24:22:00'],'RP8':[1,'22:15:00'], 'TN8':[1,'24:54:00'], 'TR3':[1,'23:53:00'], 'TZ7':[1,'23:53:00']}
# Is there an overlap actigraph recording for the sleep lab recording?
sub_list = [fn.split('_')[0] for fn in os.listdir('CSVs')]
sub_list.remove('ME5')
Subjects = []
for sub in sub_list:
    overlap = (overlap_dict.get(sub))[0]
    EEG_start_time = (overlap_dict.get(sub))[1]
    Subjects.append(Subject(sub, overlap, EEG_start_time))

pre = ['1st_', '2nd_', '3rd_']
param = ['SE','WASO','SME','TST','SPT']
dfs = []

night_list = [pd.DataFrame(columns=[pre[0]+fn for fn in param]), pd.DataFrame(columns=[pre[1]+fn for fn in param]), pd.DataFrame(columns=[pre[2]+fn for fn in param])]
overlap = pd.DataFrame(columns=param)
for i, sub in enumerate(Subjects):
    nights = sub.extract_night()
    if sub.overlap:
        overlap_night = nights.pop()
    else:
        overlap_night = sub.lab_sleep_score

    for j in range(len(nights)):
        night = nights[j]
        stats = sleep_statistics(night['SleSco'], sub.st_watch)
        for par in param:
            night_list[j].at[i, pre[j]+par] = stats.get(par)

    print('')
    stats = sleep_statistics(overlap_night['SleSco'], sub.st_watch) if sub.overlap else sleep_statistics(overlap_night, sub.st_lab)
    for par in param:
        overlap.at[i, par] = stats.get(par)

pred = pd.concat([night_list[0], night_list[1]], axis=1)[[pre[0]+'SME', pre[1]+'SME']]
to_predict = 'SE'
y = overlap['to_predict']

from sklearn.linear_model import LinearRegression
reg = LinearRegression().fit(pred, y)
y_pred = reg.predict(pred)

plt.scatter(y, y_pred, color='red')
plt.plot(y, y, color='blue', linewidth=2)
from sklearn.metrics import r2_score
r = r2_score(y, y_pred)
plt.text(60, 90, f'R squared:{round(r, 2)}')
plt.title(F{'')
plt.show()


print('')


