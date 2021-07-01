from Subject import *

from main_with_inputs import load_subject
from Statistics import get_all_night_stats

def plot_regression(y, y_pred, predictors, to_predict):
    import matplotlib.pyplot as plt

    plt.scatter(y, y_pred, color='red')
    plt.plot(y, y, color='blue', linewidth=2)
    from sklearn.metrics import r2_score
    r = r2_score(y, y_pred)
    plt.text(60, 90, f'R squared:{round(r, 2)}')
    plt.title(f'Predicting {to_predict} from EEG data with:{[fn for fn in predictors]}')
    plt.xlabel(f'{to_predict} Real values')
    plt.ylabel(f'{to_predict} Predicted values')
    plt.show()


def get_regression_analysis(predictors, to_predict, param = ['SE','WASO','SME','TST','SPT']):

    Subjects, sub_list = load_subject()
    # Removing ME5 because it has only 1 previous night
    Subjects.pop(sub_list.index('ME5'))

    night_list, overlap = get_all_night_stats(Subjects)
    pre = ['1st_', '2nd_', '3rd_']

    fin_pred = []
    for val in pre[:-1]:
        for i, j in enumerate(predictors):
            fin_pred.append(val+j)

    pred = pd.concat([night_list[0], night_list[1]], axis=1)[fin_pred]
    y = overlap[to_predict]

    from sklearn.linear_model import LinearRegression
    reg = LinearRegression().fit(pred, y)
    y_pred = reg.predict(pred)

    plot_regression(y, y_pred, predictors, to_predict)

if __name__ == "__main__":
    get_regression_analysis(['WASO', 'TST'], 'SE')

