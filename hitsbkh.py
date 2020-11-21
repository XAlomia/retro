# strikeouts homeruns and walks 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool

output_file("lines.html")




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

df = df.groupby(by = ['full_date',
                      'full_date2','bat_id']).agg({'h':'sum'})
df = df.reset_index()
df = df.merge(players, left_on = 'bat_id', right_on = 'retroID')

def debut_pkr(x):
    return int(x.debut.replace("-",""))
df['debut2'] = df.apply(debut_pkr, axis = 1) 

df = df.query("debut2 >= 19900101")

player_list = list(df.bat_id.unique())

list1 = []
list2 = []

for i, p in enumerate(player_list):
    if(i % 200 == 0): print(i)
    df_p = df[df['bat_id'] == p]
    if(df_p.shape[0] >= 500): # first 500 games  
        df_p['h_cum'] = np.cumsum(df_p.h)
        df_p = df_p.iloc[0:500:,:].reset_index()
        if(df_p.h.sum() >= 650): print(p) # many hits    
        plt.plot(df_p.h_cum, color = 'grey', alpha = .7, linewidth = .7)
        list1.append(list(df_p.retroID))
        list2.append(list(df_p.h_cum))
    
    plt.xlabel("Game of Career")
    plt.ylabel("Cumulative Hits")
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)   
    plt.gca().spines['bottom'].set_smart_bounds(True)
    plt.gca().spines['left'].set_smart_bounds(True)
    plt.grid(axis = 'y', alpha = .3)    
    plt.gcf().set_size_inches(13,5)

#bkh chart     
source = ColumnDataSource(dict(
        xs=[i for i in range(0,499)],
        ys=list2,
        nms=list1
    )
)

p = figure(title="simple line example")
p.multi_line([list(i for i in range(0,499))]*len(list1), 
              list2, line_width=2)    
p.add_tools(HoverTool(tooltips= list1))
show(p)