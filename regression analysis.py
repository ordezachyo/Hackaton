from Subject import *
import matplotlib.pyplot as plt
from main_with_inputs import load_subject



def get_regression_analysis(predictors, to_predict, param = ['SE','WASO','SME','TST','SPT']):

    Subjects, sub_list = load_subject()
    # Removing ME5 because it has only 1 previous night
    Subjects.remove(sub_list.index('ME5'))


    pre = ['1st_', '2nd_', '3rd_']
    # A list of all nights with watch features CSVs
    # The overlap night features csv
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


