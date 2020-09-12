# strikeouts homeruns and walks 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from statsmodels.stats.proportion import proportions_ztest

col_names = pd.read_csv("C:/Users/Xavier/retro/column_names.csv", 
                        header = None)
column_names = [each_string.lower() for each_string in list(col_names[0])]

read_df = \
pd.read_csv("C:/Users/Xavier/retro/all2010decade.csv", header = None, 
         names = column_names)

df = read_df.copy()

def yr_pkr(x):
    return x.game_id[3:7]

df['year'] = df.apply(yr_pkr, axis = 1)

df['h'] = np.where(df.h_fl > 0, 1, 0)
df['wlk'] = np.where(df.event_cd == 14, 1, 0) # only BB, not IBB 
df['so'] = np.where(df.event_cd == 3, 1, 0)
df['sngl'] = np.where(df.h_fl == 1, 1, 0)
df['dbl'] = np.where(df.h_fl == 2, 1, 0)
df['trpl'] = np.where(df.h_fl == 3, 1, 0)
df['hr'] = np.where(df.h_fl == 4, 1, 0)
df['pa'] = np.where(df.bat_event_fl == 'T', 1, 0)
df['ab'] = np.where(df.ab_fl == 'T', 1, 0)
df['rnrs_on'] = np.where(df.base1_run_id.isnull() & \
  df.base2_run_id.isnull() & df.base3_run_id.isnull(), 0, 1)

df = df.groupby(by = "year").agg({'hr':'sum','wlk':'sum','so':'sum','pa':\
    'sum'})
df = df.reset_index()

# current season 2020 
df = df.append({'hr':1_735,'pa':49_429,'so':11_413,'wlk':4_566,'year':2020},
               ignore_index = True)
""""""

df['so_pct'] = (df.so/df.pa) * 100               
df['wlk_pct'] = (df.wlk/df.pa) * 100  
df['hr_pct'] = (df.hr/df.pa) * 100 

plt.plot(df.so_pct[:-1], color = 'tab:red') 
plt.plot(df.wlk_pct[:-1], color = 'tab:blue')
plt.plot(df.hr_pct[:-1], color = 'tab:green')
plt.plot(list(df.index[-2:]), list(df.so_pct[-2:]), 
              color = 'tab:red', linestyle = '--')
plt.plot(list(df.index[-2:]), list(df.wlk_pct[-2:]), 
              color = 'tab:blue', linestyle = '--')
plt.plot(list(df.index[-2:]), list(df.hr_pct[-2:]), 
              color = 'tab:green', linestyle = '--')
plt.ylim(0)
plt.ylabel("% of Plate Appearancs")
plt.gcf().set_size_inches(12,5)
plt.gca().spines['top'].set_visible(False)  
plt.gca().spines['right'].set_visible(False)  
plt.gca().spines['left'].set_smart_bounds(True)  
plt.gca().spines['bottom'].set_smart_bounds(True)  
plt.grid(axis = 'y', alpha = .3)
plt.xticks(list(df.index.values), list(df.year), rotation = 45)
plt.legend(['Strikeouts','Walks','Homeruns'])


