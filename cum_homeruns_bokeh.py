from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import pandas as pd 

df = pd.read_csv('b_df.csv')

data = {'x_values': [1, 2, 3, 4, 5],
        'y_values': [6, 7, 2, 3, 6]}

source = ColumnDataSource(data=data)

p = figure()
p.circle(x='x_values', y='y_values', source=source)

p.output("test.html")
show(p)