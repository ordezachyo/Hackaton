import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Subject import *
import matplotlib.pyplot as plt
import datetime
import sys

def load_subject():
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

    return Subjects, sub_list

if __name__ == "__main__":

    print(f"Welcome to SleSco™ !\n\n") # Welcome message
    # Setting the different messages for interacting with the user
    main_menu = (f"Choose the number of the action you would you like to perform:\n\
    1. Plot Sleep Data\n\
    2. Create Prediction Model - Previous Nights -> Sleep Lab\n\
    3. Check Motionlogger to EEG Correlation\n\
    4. Examine Subjects List\n\n\
    At any time, you can go back to the main menu by typing 'main' or quit typing 'quit' \n")
    action_1=("To choose a specific subject, type his subject code\n\
    Alternativly, type 'all' to plot all subjects\n")
    action_2=("Choose the predicted variable:")
    action_2_1 = (f"Choose predictors, seperate by pressing 'Enter'. Type 'end' to finish")

    action_4=("If you would like to remove a subject, type his subject code\n\
    Reminder - you can go back to the main menu by typing 'main' or quit by typing 'quit' \n")
    reminder = ("Reminder - you can go back to the main menu by typing 'main' or quit by typing 'quit' ")
    while True:
        main_choice = (input (main_menu))
        if main_choice == 'quit':
            sys.exit("App Quit. Goodbye!")
        elif main_choice == 'main':
            continue
        try:
            main_choice = int (main_choice)
        except ValueError:
            print("Sorry, I didn't understand that.")
            #better try again... Return to the start of the loop
            continue
        if main_choice == 1:
            while True:
                choice_1 = (input (action_1))
                if choice_1 == 'quit':
                    sys.exit("App Quit. Goodbye!")
                elif choice_1 == 'main':
                    break
                elif choice_1 == 'all':
                    for sub in Subjects:
                        sub.plot_sleep_scores()
                        plt.show()
                        print (reminder)
                try:
                    is_sub=sub_list.index(choice_1)
                except:
                    print ("Subject not found. Please try again.")
                    continue
                else:
                    Subjects[is_sub].plot_sleep_scores()
                    plt.show()
                    continue
        if main_choice == 2:
            regression_flag=True
            var_list = ['SE','WASO','SME','TST','SPT']
            while regression_flag:
                print (action_2)
                print (*var_list, sep="/")
                predicted= input ()
                if predicted == 'quit':
                    sys.exit("App Quit. Goodbye!")
                elif predicted == 'main':
                    break
                try:
                    is_var=var_list.index(predicted)
                except:
                    print ("No such variable found. Please try again.")
                    continue
                else:
                    is_var=var_list.index('SE')
                    var_list.pop(is_var)
                print (action_2_1)
                print (*var_list, sep=", ")
                pre_list = []
                while True:
                    predictor=input()
                    if predictor == 'quit':
                        sys.exit("App Quit. Goodbye!")
                    elif predictor == 'main':
                        regression_flag = False
                        break
                    elif predictor=='end':
                        regression_flag = False
                        if len(pre_list)==0:
                            print('No predictors given. Returning to main menu')
                            break
                        else:
                            get_regression_analysis(pre_list,predicted)
                            break
                    try:
                        is_pre=var_list.index(predictor)
                # if the input is not in list, try again
                    except:
                        print ("No such variable found. Please try again.")
                        print ("Choose from available predictors or type 'end' to run regression")
                        print (*var_list, sep=", ")
                        continue
                    else:
                        pre_list.append(predictor)
                        var_list.pop(is_pre)
                        print ("Choose another predictor or type 'end' to run regression")
                        print (*var_list, sep=", ")

        if main_choice == 4:
            while True:
                print ("Subjects list:")
                print (sub_list)
                choice_4 = (input (action_4))
                if choice_4 == 'quit':
                    sys.exit("App Quit. Goodbye!")
                elif choice_4 == 'main':
                    break
                try:
                    is_sub=sub_list.index(choice_4)
                except:
                    print ("Subject not found. Please try again.")
                    continue
                else:
                    sub_list.pop(is_sub)
                    Subjects.pop(is_sub)
                    continue
        if main_choice>4:
            print("Sorry, I didn't understand that.")
            #better try again... Return to the start of the loop

