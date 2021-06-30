import os
import pandas as pd

sep = os.sep
sub_list = [fn for fn in os.listdir('CSVs')]
for sub in sub_list:
    csv = pd.read_csv('CSVs'+sep+sub)
    print('')
print('')