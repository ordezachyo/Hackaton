# Hackaton
**Comparing sleep patterns as measured in actigraphy versus EEG**
_Our goal is to create an application that recieves actigraph data and uses it to predict sleep quality, as represented by EEG data, in the following night_   

_Creating the data files_
1. **EEG Scoring data files should be in the following format:** ‘’subject’s initials’_hypnoWholeFile_revised.txt’ and be saved inside a file called ‘scoring_cntrl’ in ‘watch_data’.
2. **Actiograph scoring data files should be produced by ‘action4’ program:** ’sleep’> ’Automatic scoring’> save channel as ‘SleSco’ then ‘file’>’export data’ and save beginning with the subject’s initials in ‘CSVs’ folder.

_Our predicting parameters:_
**Sleep Period Time (SPT):** duration from first to last period of sleep.
**Wake After Sleep Onset (WASO):** duration of wake periods within SPT.
**Total Sleep Time (TST):** SPT - WASO.
**Sleep Maintenance Efficiency (SME):** TST / SPT * 100 (%).
