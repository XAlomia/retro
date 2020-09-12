import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from statsmodels.stats.proportion import proportions_ztest

#
read_df = \
pd.read_csv("C:/Users/Xavier/Documents/retro/all2010decade.csv", header = None)
# https://bayesball.github.io/VB/Simple_Retrosheet.html
# headers http://chadwick.sourceforge.net/doc/cwevent.html
# cwevent -y 2018 -f 0-96 2018*.EV* > all2018.csv
    
column_names = ['GAME_ID','AWAY_TEAM_ID','INN_CT','BAT_HOME_ID','OUTS_CT',
'BALLS_CT','STRIKES_CT','PITCH_SEQ_TX','AWAY_SCORE_CT','HOME_SCORE_CT','BAT_ID'
,'BAT_HAND_CD','RESP_BAT_ID','RESP_BAT_HAND_CD','PIT_ID','PIT_HAND_CD',
'RESP_PIT_ID','RESP_PIT_HAND_CD','POS2_FLD_ID','POS3_FLD_ID','POS4_FLD_ID',
'POS5_FLD_ID','POS6_FLD_ID','POS7_FLD_ID','POS8_FLD_ID','POS9_FLD_ID',
'BASE1_RUN_ID','BASE2_RUN_ID','BASE3_RUN_ID','EVENT_TX','LEADOFF_FL','PH_FL',
'BAT_FLD_CD','BAT_LINEUP_ID','EVENT_CD','BAT_EVENT_FL','AB_FL','H_FL','SH_FL',
'SF_FL','EVENT_OUTS_CT','DP_FL','TP_FL','RBI_CT','WP_FL','PB_FL','FLD_CD',
'BATTEDBALL_CD','BUNT_FL','FOUL_FL','BATTEDBALL_LOC_TX','ERR_CT','ERR1_FLD_CD',
'ERR1_CD','ERR2_FLD_CD','ERR2_CD','ERR3_FLD_CD','ERR3_CD','BAT_DEST_ID',
'RUN1_DEST_ID','RUN2_DEST_ID','RUN3_DEST_ID','BAT_PLAY_TX','RUN1_PLAY_TX',
'RUN2_PLAY_TX','RUN3_PLAY_TX','RUN1_SB_FL','RUN2_SB_FL','RUN3_SB_FL',
'RUN1_CS_FL','RUN2_CS_FL','RUN3_CS_FL','RUN1_PK_FL','RUN2_PK_FL','RUN3_PK_FL',
'RUN1_RESP_PIT_ID','RUN2_RESP_PIT_ID','RUN3_RESP_PIT_ID','GAME_NEW_FL',
'GAME_END_FL','PR_RUN1_FL','PR_RUN2_FL','PR_RUN3_FL','REMOVED_FOR_PR_RUN1_ID',
'REMOVED_FOR_PR_RUN2_ID','REMOVED_FOR_PR_RUN3_ID','REMOVED_FOR_PH_BAT_ID',
'REMOVED_FOR_PH_BAT_FLD_CD','PO1_FLD_CD','PO2_FLD_CD','PO3_FLD_CD',
'ASS1_FLD_CD','ASS2_FLD_CD','ASS3_FLD_CD','ASS4_FLD_CD','ASS5_FLD_CD',
'EVENT_ID']
column_names = [each_string.lower() for each_string in column_names]
read_df.columns = column_names 
df = read_df.copy()



def yr_pkr(x):
    return x.game_id[3:7]

read_df['year'] = read_df.apply(yr_pkr, axis = 1)
    
def yr_pkr(x):
    return x.game_id[3:7]

df['year'] = df.apply(yr_pkr, axis = 1)

df['h'] = np.where(df.h_fl > 0, 1, 0)
df['sngl'] = np.where(df.h_fl == 1, 1, 0)
df['dbl'] = np.where(df.h_fl == 2, 1, 0)
df['trpl'] = np.where(df.h_fl == 3, 1, 0)
df['hr'] = np.where(df.h_fl == 4, 1, 0)
df['pa'] = np.where(df.bat_event_fl == 'T', 1, 0)
df['ab'] = np.where(df.ab_fl == 'T', 1, 0)
df['rnrs_on'] = np.where(df.base1_run_id.isnull() & \
  df.base2_run_id.isnull() & df.base3_run_id.isnull(), 0, 1)
    
#df = df.query("year == '2017'")
df = df.groupby(by = ['year','rnrs_on']).\
agg({'h':'sum','ab':'sum','sngl':'sum','dbl':'sum','trpl':'sum','hr':'sum'})
    
df = df.pivot_table(values = ['h','ab','sngl','dbl','trpl','hr'],
                   columns = 'rnrs_on', index = 'year')

#df_slug = (df.sngl + (df.dbl * 2) + (df.trpl * 3) + (df.hr * 4))/df.ab    
df_slug = df.h/df.ab    
    
#df = df.query("ab > 500")
#df['ba'] = round(df.h/df.ab,3)
df['slg'] = round(((df.sngl) + (df.dbl * 2) + (df.trpl * 3) + (df.hr * 4))/\
            df.ab,3)

plt.plot(df_slug[0], color = 'red')
plt.plot(df_slug[1], color = 'green')
#plt.ylim(0)
#df.sort_values(by = 'ba', ascending = False)
# need bat_event_fl == T 

et = int(df.query("rnrs_on == 1").slg.values[0] * \
         df.query("rnrs_on == 1").ab.values[0])
net = int(df.query("rnrs_on == 0").slg.values[0] * \
         df.query("rnrs_on == 0").ab.values[0])
ep = df.query("rnrs_on == 1").ab.values[0]
nep = df.query("rnrs_on == 0").ab.values[0]

count = np.array([et, net])
nobs = np.array([ep, nep])
stat, pval = proportions_ztest(count, nobs)
print(df)
print(stat, pval)

# null hypothesis is both are the same 
# if p value less than .05 , reject null hypothesis 