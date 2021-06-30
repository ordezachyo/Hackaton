import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Subject import *
import matplotlib.pyplot as plt

sub = Subject('AG1')
a = sub.lab_sleep_score.replace([2,3,4,-1],1)
a = pd.DataFrame.to_numpy(a)
a = a.squeeze()


fig,ax = plt.subplots()
ax = a.plot()

print('test')