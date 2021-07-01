# Hackaton
**Comparing sleep patterns as measured in actigraphy versus EEG**<br />
_Our goal is to create an application that recieves actigraph data and uses it to predict sleep quality, as represented by EEG data, in the following night_   

_Creating the data files_
1. **EEG Scoring data files should be in the following format:** ‘’subject’s initials’_hypnoWholeFile_revised.txt’ and be saved inside a file called ‘scoring_cntrl’ in ‘watch_data’.
2. **Actiograph scoring data files should be produced by ‘action4’ program:** ’sleep’> ’Automatic scoring’> save channel as ‘SleSco’ then ‘file’>’export data’ and save beginning with the subject’s initials in ‘CSVs’ folder.

_provising subjects data into dictionary_<br />
**The user has to submit whether there was an overlaping night, and date and time of EEG recording in lab** in the '_dict' variable in 'main.py'
1. If the EEG recording night in the lab included a watch measurment, first value in the list attributed to the subject should be '1', otherwhise, enter '0'.
2. second value in the list should be in the following format: "%H:%M:%S %m/%d/%Y". For example, 00:15:00 07/02/2018.

_Our predicting parameters:_<br />
**Sleep Period Time (SPT):** duration from first to last period of sleep.<br />
**Wake After Sleep Onset (WASO):** duration of wake periods within SPT.<br />
**Total Sleep Time (TST):** SPT - WASO.<br />
**Sleep Maintenance Efficiency (SME):** TST / SPT * 100 (%).

_Our scripts_
**main_with_inputs:** Our main script 
1. Appends to subjects their CSV files with actigraph data 
2. Adds information about overlaping nights (actigraph+EEG data), hour & date of EEG recording nights at the lab 
3. Contains all the instructions by our UI
4. Plots sleep data for subject\s according to user's request
5. Creats a prediction model for EEG data by actigraph based on chosen sleep 
    parameters
6. Creats a correlation matrix
7. Shows the subject list

**Statistics** Pulls the data (sleep parameters from yasa) and plots the correlation matrix. Calculates regression model.

**Subject** Creats a class Subject that integrates all of each subject's data. 

**testing_script** Includes tests to assure the code's validity