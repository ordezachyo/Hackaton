import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Subject import *
import matplotlib.pyplot as plt
import datetime
import sys

def load_subject():
    overlap_dict = {'AG1': [1, '23:48:00 07/25/2018'], 'CS7': [1, '21:29:00 10/23/2018'],
                    'DS6': [1, '22:41:00 08/19/2018'],
                    'EC0': [1, '23:54:00 08/28/2018'], 'EG5': [1, '23:10:00 03/04/2018'],
                    'HS0': [1, '23:30:00 07/17/2018'],
                    'JR9': [1, '22:48:00 02/18/2018'], 'ME5': [0, '23:46:00 04/24/2018'],
                    'MK2': [1, '22:32:00 11/19/2018'],
                    'NS6': [0, '00:22:00 03/19/2018'], 'RP8': [1, '22:15:00 02/23/2018'],
                    'TN8': [1, '00:54:00 01/16/2018'],
                    'TR3': [1, '23:53:00 10/14/2018'], 'TZ7': [1, '23:53:00 04/10/2018']}

    sub_list = [fn.split('_')[0] for fn in os.listdir('CSVs')]

    date_format_string = "%H:%M:%S %m/%d/%Y"

    for sub in sub_list:
        overlap = (overlap_dict.get(sub))[0]
        EEG_start_time = datetime.datetime.strptime((overlap_dict.get(sub))[1], date_format_string)
        Subjects.append(Subject(sub, overlap, EEG_start_time))

    return Subjects, sub_list


print('Loading...')
Subjects = []

# Is there an overlap actigraph recording for the sleep lab recording?

Subjects, sub_list = load_subject(overlap_dict)

print(f"Welcome to SleSco™ !\n\n")
main_menu = (f"Choose the number of the action you would you like to perform:\n\
1. Plot Sleep Data\n\
2. Create Prediction Model - Previous Nights -> Sleep Lab\n\
3. Check Motionlogger to EEG Correlation\n\
4. Examine Subjects List\n\n\
At any time, you can go back to the main menu by typing 'main' or quit typing 'quit' \n")
action_1=("To choose a specific subject, type his subject code\n\
Alternativly, type 'all' to plot all subjects\n")
action_4=("If you would like to remove a subject, type his subject code\n\
Reminder - you can go back to the main menu by typing 'main' or quit by typing 'quit' \n")
reminder = ("Reminder - you can go back to the main menu by typing 'main' or quit by typing 'quit' ")
while True:
    choice = (input (main_menu))
    if choice == 'quit':
        sys.exit("App Quit. Goodbye!")
    elif choice == 'main':
        continue
    try:
        choice = int (choice)
    except ValueError:
        print("Sorry, I didn't understand that.")
        #better try again... Return to the start of the loop
        continue       
    if choice == 1:
        while True:
            choice = (input (action_1))
            if choice == 'quit':
                sys.exit("App Quit. Goodbye!")
            elif choice == 'main':
                break
            elif choice == 'all':
                for sub in Subjects:
                    sub.plot_sleep_scores()
                    plt.show()
                    print (reminder)
            try:
                is_sub=sub_list.index(choice)
            except:
                print ("Subject not found. Please try again.")
                continue
            else:
                Subjects[is_sub].plot_sleep_scores()
                plt.show()
                continue
    if choice == 4:
        while True:
            print ("Subjects list:")
            print (sub_list)
            choice = (input (action_4))
            if choice == 'quit':
                sys.exit("App Quit. Goodbye!")
            elif choice == 'main':
                break
            try:
                is_sub=sub_list.index(choice)
            except:
                print ("Subject not found. Please try again.")
                continue
            else:
                sub_list.pop(is_sub)
                Subjects.pop(is_sub)
                continue
    if choice>4:
        print("Invalid choice. Plesase try again")
        #better try again... Return to the start of the loop
        continue 
