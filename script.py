import os
import re
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import GetHistoryRequest
import telegram_functions

api_id = 1787001
api_hash = 'd8aa74a3fa79f398b55becc413b4ecee'

client = TelegramClient('session_name', api_id, api_hash)

client.start()

print('Collating channel list...')
retrieved_channel_ids, channel_list = telegram_functions.prepare_for_harvest()
restricted_channels = list()
print('Done!')

'''
with open('channels_to_get.txt', 'r') as f:
    channel_list = f.read().split('\n')
f.close()
new_channel_list = channel_list
for x in channel_list:
    try:
        int(x)
    except:
        new_channel_list.remove(x)
channel_list = [int(x) for x in new_channel_list]
text_files = [tf for tf in os.listdir() if tf.endswith('txt') and not tf.startswith('channels')]
print(text_files)
retrieved_channel_ids = [int(re.search('([0-9]+)\\_.*$', x).group(1)) for x in text_files]
'''

print(len(channel_list))
retrieved_channel_ids = telegram_functions.recursive_get_channel_messages(api_id, api_hash, channel_list, retrieved_channel_ids, client)

with open('retrieved_channels', 'w') as f:
  f.write('\n'.join(retrieved_channel_ids))
