from Subject import *
import matplotlib.pyplot as plt
from main_with_inputs import load_subject
from Statistics import get_all_night_stats
from yasa import sleep_statistics
from main_with_inputs import load_subject
import seaborn as sns




def get_corr_data( param = ['SE','WASO','SME','TST','SPT']):
    '''
    #This function pulls the data for the correlation matrix
    :param param: list of statistics to include in the plot
    :return: Subject: a list of all the subjects, sub_list: a list of all the subjects names, overlap: DataFrame of the overlap night, night_lab: DataFrame of the night in the lab
    '''
    Subjects, sub_list = load_subject()
    # Removing ME5 because it has only 1 previous night
    Subjects.pop(sub_list.index('ME5'))

    night_list, night_lab, overlap = get_all_night_stats(Subjects, param)
    return  Subjects,sub_list,overlap,night_list,night_lab

def corr_plot():
    '''
    This function plots the correlation matrix for all the data
    :return: none
    '''

    param = ['SE','WASO','SME','TST','SPT']
    Subjects, sub_list, overlap, night_list,night_lab = get_corr_data(param)

    night_list.append(night_lab) # Add statistics from the lab before concat all data

    df_all = pd.concat(night_list, axis=1)
    df_all - pd.concat([df_all,night_lab], axis = 1)

    df_all.drop(['1st_SE','2nd_SE','3rd_SE','3rd_WASO','3rd_SME','3rd_TST','3rd_SPT'] ,axis = 1, inplace = True) # Drop all shit

    # Add means col

    df_all['mean_SPT'] = df_all[['1st_SPT', '2nd_SPT']].mean(axis=1)
    df_all['mean_WASO'] = df_all[['1st_WASO', '2nd_WASO']].mean(axis=1)
    df_all['mean_TST'] = df_all[['1st_TST', '2nd_TST']].mean(axis=1)
    df_all['mean_SME'] = df_all[['1st_SME', '2nd_SME']].mean(axis=1)

    # Change some col names

    df_all.rename( columns ={'SE' : 'SE_Lab', 'SME' :'SME_LAB','TST':'TST_Lab','SPT':'SPT_LAB','WASO':'WASO_Lab'}, inplace=True)


    corr_matrix = df_all.astype(float).corr()

    fig, ax = plt.subplots(figsize=(12, 9))
    fig.suptitle('Correlation Matrix')
    sns.set(font_scale=1)
    sns.heatmap(corr_matrix, annot=True,annot_kws = {"size": 10},cmap = 'coolwarm',square = True)
    plt.show()



