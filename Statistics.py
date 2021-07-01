from Subject import *
import matplotlib.pyplot as plt
import seaborn as sns

def get_all_night_stats(Subjects, param = ['SE','WASO','SME','TST','SPT']):
    from yasa import sleep_statistics
    import pandas as pd
    pre = ['1st_', '2nd_', '3rd_', 'Watch_']

    # A list of all nights with watch features CSVs
    # The overlap night features csv
    night_list = [pd.DataFrame(columns=[pre[0] + fn for fn in param]+['Name']),
                  pd.DataFrame(columns=[pre[1] + fn for fn in param]+['Name']),
                  pd.DataFrame(columns=[pre[2] + fn for fn in param]+['Name'])]

    lab_eeg = pd.DataFrame(columns=param)
    overlap_night = pd.DataFrame(columns=[pre[2] + fn for fn in param]+['Name'])



    for i, sub in enumerate(Subjects):
        nights = sub.nights
        if sub.overlap:
            o_night = nights.pop()
            o_stats = sleep_statistics(o_night['SleSco'], sub.st_watch)

        for j in range(len(nights)):
            night = nights[j]
            stats = sleep_statistics(night['SleSco'], sub.st_watch)
            for par in param:
                night_list[j].at[i, pre[j] + par] = stats.get(par)
                if sub.overlap:
                    overlap_night.at[i, pre[-1]+par] = o_stats.get(par)
                    overlap_night.at[i, 'Name'] = sub.name
            night_list[j].at[i, 'Name'] = sub.name

        lab_stats = sleep_statistics(sub.lab_sleep_score, sub.st_lab)

        for par in param:
            lab_eeg.at[i, par] = lab_stats.get(par)
            lab_eeg.at[i, 'Name'] = sub.name

    for night in night_list:
        night.set_index('Name', inplace=True)
    lab_eeg.set_index('Name', inplace=True)
    overlap_night.set_index('Name', inplace=True)

    return night_list, lab_eeg, overlap_night

def plot_regression(y, y_pred, predictors, to_predict):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plt.scatter(y, y_pred, color='red')
    plt.plot(y, y, color='blue', linewidth=2)
    from sklearn.metrics import r2_score
    r = round(r2_score(y, y_pred), 3)
    fig.suptitle(f'Predicting {to_predict} from EEG data with:{[fn for fn in predictors]}, R squared:{r}', fontsize=10)
    plt.xlabel(f'{to_predict} Real values')
    plt.ylabel(f'{to_predict} Predicted values')
    plt.tight_layout()
    plt.show()

# Regression analysis
def get_regression_analysis(predictors, to_predict, Subjects):
    from main_with_inputs import load_subject
    from Statistics import get_all_night_stats
    import pandas as pd

    night_list, lab_eeg, _ = get_all_night_stats(Subjects)
    pre = ['1st_', '2nd_', '3rd_']

    fin_pred = []
    for val in pre[:-1]:
        for i, j in enumerate(predictors):
            fin_pred.append(val+j)

    pred = pd.concat([night_list[0], night_list[1]], axis=1)[fin_pred]
    y = lab_eeg[to_predict]

    from sklearn.linear_model import LinearRegression

    try:
        reg = LinearRegression().fit(pred, y)
        y_pred = reg.predict(pred)
    except ValueError:
        print('Data contains Nan')
    plot_regression(y, y_pred, predictors, to_predict)

# Correlations analysis
def get_corr_data(param=['SE', 'WASO', 'SME', 'TST', 'SPT']):
    '''
    #This function pulls the data for the correlation matrix
    :param param: list of statistics to include in the plot
    :return: Subject: a list of all the subjects, sub_list: a list of all the subjects names, overlap: DataFrame of the overlap night, night_lab: DataFrame of the night in the lab
    '''
    from main_with_inputs import load_subject
    Subjects, sub_list = load_subject()
    # Removing ME5 because it has only 1 previous night
    Subjects.pop(sub_list.index('ME5'))

    night_list, night_lab, overlap = get_all_night_stats(Subjects, param)
    return Subjects, sub_list, overlap, night_list, night_lab


def corr_mean_lab():
    '''
    This function plots the correlation matrix for all the data
    :return: none
    '''
    param = ['SE', 'WASO', 'SME', 'TST', 'SPT']
    Subjects, sub_list, overlap, night_list, night_lab = get_corr_data(param)

    night_list.append(night_lab)  # Add statistics from the lab before concat all data

    df_all = pd.concat(night_list, axis=1)
    df_all - pd.concat([df_all, night_lab], axis=1)

    df_all.drop(['1st_SE', '2nd_SE', '3rd_SE', '3rd_WASO', '3rd_SME', '3rd_TST', '3rd_SPT'], axis=1,
                inplace=True)  # Drop all shit

    # Add means col

    df_all['mean_SPT'] = df_all[['1st_SPT', '2nd_SPT']].mean(axis=1)
    df_all['mean_WASO'] = df_all[['1st_WASO', '2nd_WASO']].mean(axis=1)
    df_all['mean_TST'] = df_all[['1st_TST', '2nd_TST']].mean(axis=1)
    df_all['mean_SME'] = df_all[['1st_SME', '2nd_SME']].mean(axis=1)

    # Change some col names
    df_all.drop(['2nd_WASO', '2nd_SME', '2nd_TST', '2nd_SPT', '1st_WASO', '1st_SME', '1st_TST', '1st_SPT'], axis=1,
                inplace=True)
    df_all.rename(columns={'SE': 'EEG_SE', 'SME': 'EEG_SME', 'TST': 'EEG_TST', 'SPT': 'EEG_SPT', 'WASO': 'EEG_WASO'},
                  inplace=True)

    corr_matrix = df_all.astype(float).corr()

    fig, ax = plt.subplots(figsize=(12, 9))
    fig.suptitle('Correlation Matrix of Mean Watch data and EEG Data')
    sns.set(font_scale=1)
    sns.heatmap(corr_matrix, annot=True, annot_kws={"size": 10}, cmap='coolwarm')
    plt.show()


def corr_lab_night():
    '''
    This function plots the correlation matrix of the lab night's data from the watch and EEG
    :return: none
    '''
    param = ['SE', 'WASO', 'SME', 'TST', 'SPT']
    Subjects, sub_list, overlap, night_list, night_lab = get_corr_data(param)
    df_all = pd.concat([night_lab, overlap], axis=1)
    df_all.drop(['3rd_SE', '3rd_WASO', '3rd_SME', '3rd_TST', '3rd_SPT'], axis=1, inplace=True)  # Drop all shit
    df_all.rename(columns={'SE': 'EEG_SE', 'SME': 'EEG_SME', 'TST': 'EEG_TST', 'SPT': 'EEG_SPT', 'WASO': 'EEG_WASO'},
                  inplace=True)
    corr_matrix = df_all.astype(float).corr()

    fig, ax = plt.subplots(figsize=(12, 9))
    fig.suptitle('Correlation Matrix of Lab Night')
    sns.set(font_scale=1)
    sns.heatmap(corr_matrix, annot=True, annot_kws={"size": 10}, cmap='coolwarm')
    plt.show()


def corr_between_nights():
    '''
    This function plots the correlation matrix of the lab night's data from the watch and EEG
    :return: none
    '''
    param = ['SE', 'WASO', 'SME', 'TST', 'SPT']
    Subjects, sub_list, overlap, night_list, night_lab = get_corr_data(param)
    df_all = pd.concat(night_list, axis=1)
    df_all.drop(['3rd_SE', '3rd_WASO', '3rd_SME', '3rd_TST', '3rd_SPT'], axis=1, inplace=True)  # Drop all shit
    # night_lab.rename( columns ={'SE' : 'EEG_SE', 'SME' :'EEG_SME','TST':'EEG_TST','SPT':'EEG_SPT','WASO':'EEG_WASO'}, inplace=True)
    corr_matrix = df_all.astype(float).corr()

    fig, ax = plt.subplots(figsize=(12, 9))
    fig.suptitle('Correlation Between Data From Two Watch Nights')
    sns.set(font_scale=1)
    sns.heatmap(corr_matrix, annot=True, annot_kws={"size": 10}, cmap='coolwarm')
    plt.show()