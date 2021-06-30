import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Subject import *
import matplotlib.pyplot as plt

Subjects = []
sub_list=[fn.split('_')[0] for fn in os.listdir('CSVs')]
for sub in sub_list:
            Subjects.append(Subject(sub))
