# strikeouts homeruns and walks 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from statsmodels.stats.proportion import proportions_ztest

col_names = pd.read_csv("C:/Users/Xavier/retro/column_names.csv", 
                        header = None)
column_names = [each_string.lower() for each_string in list(col_names[0])]

read_df = \
pd.read_csv("C:/Users/Xavier/retro/all1990_2019.csv", header = None, 
         names = column_names)

players = pd.read_csv("retro/people.csv", 
                          usecols = ['retroID','debut'])

def full_date_pkr(x):
    return int(x.game_id[3:11])

def full_date_pkr2(x):
    return int(x.game_id[3:12])

read_df['full_date'] = read_df.apply(full_date_pkr, axis = 1)
read_df['full_date2'] = read_df.apply(full_date_pkr2, axis = 1)

df = read_df.copy()

df['h'] = np.where(df.h_fl > 0, 1, 0)
#df['wlk'] = np.where(df.event_cd == 14, 1, 0) # only BB, not IBB 
#df['so'] = np.where(df.event_cd == 3, 1, 0)
#df['sngl'] = np.where(df.h_fl == 1, 1, 0)
#df['dbl'] = np.where(df.h_fl == 2, 1, 0)
#df['trpl'] = np.where(df.h_fl == 3, 1, 0)
df['hr'] = np.where(df.h_fl == 4, 1, 0)
#df['pa'] = np.where(df.bat_event_fl == 'T', 1, 0)
#df['ab'] = np.where(df.ab_fl == 'T', 1, 0)

df = df.groupby(by = ['full_date',
                      'full_date2','bat_id']).agg({'hr':'sum'})
df = df.reset_index()
df = df.merge(players, left_on = 'bat_id', right_on = 'retroID')

def debut_pkr(x):
    return int(x.debut.replace("-",""))
df['debut2'] = df.apply(debut_pkr, axis = 1) 

df = df.query("debut2 >= 20000101")

player_list = list(df.bat_id.unique())

for i, p in enumerate(player_list):
    if(i % 200 == 0): print(i)
    df_p = df[df['bat_id'] == p]
    if(df_p.shape[0] >= 500):
        df_p['hr_cum'] = np.cumsum(df_p.hr)
        df_p = df_p.iloc[0:500:,:].reset_index()
        if(df_p.hr.sum() >= 650): print(p)        
        plt.plot(df_p.hr_cum, color = 'grey', alpha = .7, linewidth = .7)
    
    plt.xlabel("Game of Career")
    plt.ylabel("Cumulative Homeruns")
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)   
    plt.gca().spines['bottom'].set_smart_bounds(True)
    plt.gca().spines['left'].set_smart_bounds(True)
    plt.grid(axis = 'y', alpha = .3)    
    plt.gcf().set_size_inches(13,5)