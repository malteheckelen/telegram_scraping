import os
import re
import json
import datetime
import pandas as pd

def make_network_from_forwards(filename):
    filenames = os.listdir()
    if filename not in filenames:
        print('Generating file.')
        os.system('touch {}'.format(filename))
    else:
        print('File already exists, compiling list of parsed channels.')
        fwd_network = pd.read_csv(filename)
        unique_ids = [int(x) for x in list(set(fwd_network.iloc[:,0]))]
    channels = [tf for tf in filenames if tf.endswith('txt')]
    counter = 1
    for channel in channels:
        try:
            channel_id = int(re.search('([0-9]+)\\_.*$', channel).group(1)) 
        except:
            continue
        if channel_id in unique_ids:
            print('Channel already parsed')
            continue
        try:
            channel_name = re.search('[0-9]+\\_(.*)\\.txt$', channel).group(1)
        except:
            channel_name = 'NAME_UNKNOWN'
        print(' '.join(['Parsing channel', str(counter), '/', str(len(channels)), ':', channel_name]))
        channel_messages = []
        with open(channel, 'r') as f:
            channel_messages = f.read().split(';;;\n;;;')
        f.close()
        channel_messages = [eval(x) for x in channel_messages]
        channel_forwards = []
        for message in channel_messages:
            if ('fwd_from' in message.keys()) and (message['fwd_from'] is not None):
                channel_forwards.append(','.join([str(channel_id), str(message['fwd_from']['channel_id']), message['date'].strftime("%m/%d/%Y %H:%M:%S")]))
        channel_forwards = '\n'.join(channel_forwards)
        with open(filename, 'a') as f:
            f.write(''.join(['\n', channel_forwards]))
        f.close()
        counter+=1

make_network_from_forwards('forward_network.csv')
