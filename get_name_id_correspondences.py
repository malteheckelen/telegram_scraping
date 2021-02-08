import os
import re
import json
import datetime
import pandas as pd


filenames = os.listdir()
channels = [tf for tf in filenames if tf.endswith('txt')]
channel_df = pd.DataFrame(data={
    'Id':[],
    'Label':[]
    })
for channel in channels:
    try:
        channel_id = str(re.search('([0-9]+)\\_.*$', channel).group(1)) 
    except:
        print('continues')
        continue
    try:
        channel_name = re.search('[0-9]+\\_(.*)\\.txt$', channel).group(1)
    except:
        channel_name = 'NAME_NOT_ALPHANUMERIC'
    channel_df = channel_df.append(pd.DataFrame(data={
        'Id':[channel_id],
        'Label':[channel_name]
        }), ignore_index=True)
    print(channel_df)

channel_df.to_csv('channel_ids_names.csv', index=False)
