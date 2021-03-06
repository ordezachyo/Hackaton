import sys
from Statistics import *
import datetime
import matplotlib.pyplot as plt


def load_subject():
    '''
    This function appends to subjects their CSV files with actigraph data, and information about
    overlaping nights (actigraph+EEG data), hour & date of EEG recording nights at the lab
    :return:
    Class subjects with full information (actigraph, EEG data, all hours and dates) and a list of CSV
    files containing actigraph data.
    '''
    overlap_dict = {'AG1': [1, '23:48:00 07/25/2018'], 'CS7': [1, '21:29:00 10/23/2018'],
                    'DS6': [1, '22:41:00 08/19/2018'], 'EC0': [1, '23:54:00 08/28/2018'],
                    'EG5': [1, '23:10:00 03/04/2018'], 'HS0': [1, '23:30:00 07/17/2018'],
                    'JR9': [1, '22:48:00 02/18/2018'], 'ME5': [0, '23:46:00 04/24/2018'],
                    'MK2': [1, '22:32:00 11/19/2018'], 'NS6': [0, '00:22:00 03/19/2018'],
                    'RP8': [1, '22:15:00 02/23/2018'], 'TN8': [1, '00:54:00 01/16/2018'],
                    'TR3': [1, '23:53:00 10/14/2018'], 'TZ7': [1, '23:53:00 04/10/2018']}

    # Is there an overlap actigraph recording for the sleep lab recording?
    sub_list = [fn.split('_')[0] for fn in os.listdir('CSVs')]
    date_format_string = "%H:%M:%S %m/%d/%Y"
    Subjects = []

    for sub in sub_list:
        overlap = (overlap_dict.get(sub))[0]
        EEG_start_time = datetime.datetime.strptime((overlap_dict.get(sub))[1], date_format_string)
        Subjects.append(Subject(sub, overlap, EEG_start_time))

    # Removing Subjects with only one night
    nights_length = [len(sub.nights) for sub in Subjects]
    one_night_indices = [i for i, x in enumerate(nights_length) if x == 1]

    while len(one_night_indices) > 0:
        Subjects.pop(one_night_indices.pop(0))
        nights_length = [len(sub.nights) for sub in Subjects]
        one_night_indices = [i for i, x in enumerate(nights_length) if x == 1]

    sub_list = [sub.name for sub in Subjects]

    return Subjects, sub_list


def instructions():
    '''
    This function contains all the instructions by our UI.
    :return:
    Different string variables with instructions for different options to analyse the data.
    '''
    # Setting the different messages for interacting with the user
    print("Welcome to SleSco??? !\n\n")  # Welcome message
    main_menu_prompt = ("Choose the number of the action you would you like to perform:\n\
        1. Plot Sleep Data\n\
        2. Create Prediction Model - Previous Nights -> Sleep Lab\n\
        3. Check Correlations\n\
        4. Examine Subjects List\n\n\
        At any time, you can go back to the main menu by typing 'main' or quit typing 'quit' \n")
    action_1 = ("To choose a specific subject, type his subject code\n\
        Alternativly, type 'all' to plot all subjects\n")
    action_2 = ("Choose the predicted variable:")
    action_2_1 = ("Choose predictors, seperate by pressing 'Enter'. Type 'end' to finish")
    action_3 = ("Which correlation would you like to check?\n\
        1. Previous nights means (Motionlogger watch) to sleep lab night recording (EEG)\n\
        2. Motionlogger to EEG - within sleep lab night recording\n\
        3. Motionlogger watch data - 1st to 2nd night recordings\n ")
    action_3_1 = ("Creating correlation matrix - Previous Nights -> Sleep Lab")
    action_3_2 = ("Creating correlation matrix - Within Sleep Lab")
    action_3_3 = ("Creating correlation matrix - Within Motionlogger watch")
    action_4 = ("If you would like to remove a subject, type his subject code\n\
        Reminder - you can go back to the main menu by typing 'main' or quit by typing 'quit' \n")
    reminder = ("Reminder - you can go back to the main menu by typing 'main' or quit by typing 'quit'\n ")
    return main_menu_prompt, action_1, action_2, action_2_1, action_3, action_3_1, action_3_2, action_3_3, action_4, reminder


def main_menu():
    '''
    This function responds to the instruction 'quit'

    :return:
    main_choice - user's choice for main menu
    '''
    main_choice = (input(main_menu_prompt))  # User's choice for main menu
    if main_choice.lower() == 'quit':
        sys.exit("App Quit. Goodbye!")

    return main_choice


def plot_sleep_data():
    '''
    This function plots sleep data for subject\s according to user's request
    :return:
    None
    '''
    while True:
        choice_1 = (input(action_1))  # User's choice within action 1
        if choice_1.lower() == 'quit':
            sys.exit("App Quit. Goodbye!")
        elif choice_1.lower() == 'main':
            break
        elif choice_1.lower() == 'all':
            for sub in Subjects:
                sub.plot_sleep_scores()
                plt.show()
            print(reminder)
        else:
            try:
                is_sub = sub_list.index(choice_1.upper())
            except:
                print("Subject not found. Please try again.")
                continue
            else:
                Subjects[is_sub].plot_sleep_scores()
                continue


def check_correlations():
    while True:
        choice_3 = input(action_3)
        if choice_3.lower() == 'quit':
            sys.exit("App Quit. Goodbye!")
        elif choice_3.lower() == 'main':
            break
        try:
            choice_3 = int(choice_3)
        except ValueError:
            print("Sorry, I didn't understand that.")
            # better try again... Return to the start of the loop
            continue
        else:
            if choice_3 == 1:
                print(action_3_1)
                corr_mean_lab()
                break
            elif choice_3 == 2:
                print(action_3_2)
                corr_lab_night()
                break
            elif choice_3 == 3:
                print(action_3_3)
                corr_between_nights()
                break
            else:
                print("Sorry, I didn't understand that.")
                print(reminder)
                # better try again... Return to the start of the loop
                continue


def run_prediction_model():
    '''
    This function creats a prediction model for EEG data by actigraph based on chosen sleep
    parameters
    :return:None
    '''
    regression_flag = True  # tracks whether regression is completed or quit
    var_list = ['SE', 'WASO', 'SME', 'TST', 'SPT']  # possible variables to predict
    while regression_flag:
        print(action_2)
        print(*var_list, sep="/")
        predicted = input()
        if predicted.lower() == 'quit':
            sys.exit("App Quit. Goodbye!")
        elif predicted.lower() == 'main':
            break
        try:
            is_var = var_list.index(predicted.upper())
        except:
            print("No such variable found. Please try again.")
            continue
        else:
            is_var = var_list.index('SE')
            var_list.pop(is_var)  # possible predictor variables - SE not included
        print(action_2_1)
        print(*var_list, sep=", ")
        pre_list = []  # chosen predictors list
        while True:
            predictor = input()
            if predictor.lower() == 'quit':
                sys.exit("App Quit. Goodbye!")
            elif predictor.lower() == 'main':
                regression_flag = False
                break
            elif predictor.lower() == 'end':  # user is ready to run regression
                regression_flag = False  # ready to go back to main menu soon
                if len(pre_list) == 0:  # regression quit
                    print('No predictors given. Returning to main menu')
                    break
                else:  # good to go
                    print(
                        f"Running linear regression to predict '{predicted.upper()}' - measured in sleep lab, using previous nights {pre_list}")
                    get_regression_analysis(pre_list, predicted.upper())  # running regression
                    break
            try:
                is_pre = var_list.index(predictor.upper())
            # if the input is not in list, try again
            except:
                print("No such variable found. Please try again.")
                print("Choose from available predictors or type 'end' to run regression")
                print(*var_list, sep=", ")
                continue
            else:
                pre_list.append(predictor.upper())
                var_list.pop(is_pre)
                if len(var_list) == 0:
                    print("No predictors left. Type 'end' to run regression")
                else:
                    print("Choose another predictor or type 'end' to run regression")
                    print(*var_list, sep=", ")


def show_subjects_list(Subjects):
    '''
    This function shows the subject list
    :return: None
    '''
    print("Subjects list:")
    sub_list = [sub.name for sub in Subjects]
    print(sub_list)


if __name__ == "__main__":
    Subjects, sub_list = load_subject()
    main_menu_prompt, action_1, action_2, action_2_1, action_3, action_3_1, action_3_2, action_3_3, action_4, reminder = instructions()

    while True:
        main_choice = main_menu()

        if main_choice.lower() == 'main':
            continue

        try:
            main_choice = int(main_choice)
        except ValueError:
            print("Sorry, I didn't understand that.")
            # better try again... Return to the start of the loop
            continue

        if main_choice == 1:  # 1.plot sleep data
            plot_sleep_data()

        if main_choice == 2:  # 2.Create Prediction Model
            try:
                run_prediction_model()
            except ValueError:
                print('Data contains Nan')

        if main_choice == 3:  # 3. Check Correlations
            check_correlations()

        if main_choice == 4:  # 4. Examine Subjects List
            show_subjects_list(Subjects)

        if main_choice > 4 or main_choice <= 0:  # input is integer but out of range
            print("Sorry, I didn't understand that.")
            # better try again... Return to the start of the loop

