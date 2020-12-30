
import numpy as np
import pandas as pd
import os
import re
from tkinter import *
from tkinter import filedialog


### add interactive directory choose

root = Tk()
directory = filedialog.askdirectory(title = 'Select a Folder')
files = [i for i in os.listdir(directory) if 'fiji.csv' in i]


df = pd.read_csv(directory + '/' + files[0]).set_index('Label').drop(columns = {' '})

filenames = df.index
delimiters = "_", "."
regexPattern = '|'.join(map(re.escape, delimiters))

count = -1
channel = [''] * len(filenames)
timepoint = [''] * len(filenames)
well_id = [''] * len(filenames)

for i in filenames:
    count += 1
    well_id[count] = i[0:3] + i[8:9]
    z = re.split(regexPattern, i)
    channel[count] = z[4]
    timepoint[count] = z[5]
    
    
df['channel'] = channel
df['timepoint'] = timepoint
df['well_id'] = well_id

#gfp = df[df['channel'] == 'GFP'][['timepoint', 'Mean', 'well_id']]
rfp = df[df['channel'] == 'RFP'][['timepoint', 'Mean', 'well_id']]

#gfp.set_index(['timepoint', 'well_id'], inplace = True)
rfp.set_index(['timepoint', 'well_id'], inplace = True)

#gfp.rename(columns = {'Mean' : 'GFP_mean'}, inplace = True)
rfp.rename(columns = {'Mean' : 'RFP_mean'}, inplace = True)

#norm_df = gfp.join(rfp).dropna()
#norm_df['RFP/GFP Ratio'] = norm_df['RFP_mean'] / norm_df['GFP_mean']
norm_df = rfp
norm_df.reset_index(inplace = True)

norm_df2 = norm_df.melt(var_name = 'label', value_name = 'mean', id_vars = ['timepoint', 'well_id'])

norm_df_final = norm_df2.pivot_table(index = ['label', 'timepoint'], columns = 'well_id')


## writing the organized dataframe out to a csv file
norm_df_final.to_csv(directory + '/python_processed_data.csv')

print('All Done! You can find the processed output here:'+ directory + '/python_processed_data.csv') 