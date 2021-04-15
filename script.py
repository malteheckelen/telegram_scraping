import os
import re
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import GetHistoryRequest
import telegram_functions

api_id = 
api_hash = 

client = TelegramClient('session_name', api_id, api_hash)

client.start()

print('Collating channel list...')
retrieved_channel_ids, channel_list = telegram_functions.prepare_for_harvest()
restricted_channels = list()
print('Done!')

print(len(channel_list))
retrieved_channel_ids = telegram_functions.recursive_get_channel_messages(api_id, api_hash, channel_list, retrieved_channel_ids, client)

with open('retrieved_channels', 'w') as f:
  f.write('\n'.join(retrieved_channel_ids))
