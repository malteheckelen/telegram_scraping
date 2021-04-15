import os
import re
import json
import datetime
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import GetHistoryRequest

def recursive_get_channel_messages(api_id, api_hash, channel_list, retrieved_channel_ids, client):
  
    new_channel_list = list()
      
    for channel_id in channel_list:
        try:
            seed_channel = client.get_entity(channel_id)
        except:
            print(' '.join([str(channel_id), 'is not reachable!']))
            continue
        retrieved_channel_ids.append(channel_id)
        try:
            if not seed_channel.restricted:
                print(' '.join(['Getting channel', ''.join([x for x in seed_channel.title if x.isalpha()])]))
                all_messages = list()
                new_local_channel_list = list()
                posts = client(GetHistoryRequest(
                    peer=seed_channel,
                    limit=9999999,
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0))
                
                for chat in posts.chats:
                  for message in client.iter_messages(chat):
                    all_messages.append(str(message.to_dict()))
                    if message.forward:
                        if (message.forward.channel_id not in retrieved_channel_ids) and (message.forward.channel_id not in new_channel_list):
                          new_local_channel_list.append(message.forward.channel_id)
                # only get new channels if they make up a somewhat sizeable fraction of forwards
                new_local_channel_list = [x for x in new_local_channel_list if new_local_channel_list.count(x) / len(new_local_channel_list) > .01]
                new_channel_list.extend([x for x in new_local_channel_list if x not in new_channel_list])
                with open(''.join(['_'.join([str(seed_channel.id), ''.join([x for x in seed_channel.title if x.isalpha()])]), '.txt']), 'w') as f:
                    f.write(';;;\n;;;'.join(all_messages))
                f.close()
            else:
              continue
        except:
            continue
        
    if new_channel_list:
      retrieved_channel_ids = recursive_get_channel_messages(api_id, api_hash, new_channel_list, retrieved_channel_ids, client)
    
    return(retrieved_channel_ids)

def prepare_for_harvest():
    text_files = [tf for tf in os.listdir() if tf.endswith('txt')]
    seen = [int(re.search('([0-9]+)\\_.*$', x).group(1)) for x in text_files]
    channels_to_get = []
    for text_file in text_files:
        channel_messages = []
        with open(text_file, 'r') as f:
            channel_messages = f.read().split(';;;\n;;;')
        f.close()
        channel_messages = [eval(x) for x in channel_messages]
        channels_to_get_local = []
        for message in channel_messages:
            if ('fwd_from' in message.keys()) and (message['fwd_from'] is not None):
                if (message['fwd_from']['channel_id'] not in seen) and (message['fwd_from']['channel_id'] not in channels_to_get):
                    channels_to_get_local.append(message['fwd_from']['channel_id']) 
        channels_to_get_local = [x for x in channels_to_get_local if channels_to_get_local.count(x) / len(channels_to_get_local) > .01]
        channels_to_get.extend(channels_to_get_local)
    channels_to_get = list(set(channels_to_get))
    return(seen, channels_to_get)

def load_channel(filename, foldername):
    channel_messages = []
    with open(''.join([foldername, '/', text_file]), 'r') as f:
        channel_messages = f.read().split(';;;\n;;;')
    f.close()
    channel_messages = [eval(msg)['text'] for msg in channel_messages]
    return channel_messages
    
def update_channels(client, foldername):
    text_files = [tf for tf in os.listdir('backup') if tf.endswith('txt')]
    
    for text_file in text_files:
        channel_id = int(re.search('(^.*?)_.*$', text_file).group(1))
        print(channel_id)
        channel_messages = []
        with open(''.join([foldername, '/', text_file]), 'r') as f:
            channel_messages = f.read().split(';;;\n;;;')
        f.close()
        start_date = max([eval(msg)['date'] for msg in channel_messages])
        try:
            channel = client.get_entity(channel_id)
            print(' '.join([text_file, 'is reached!']))
        except:
            print(' '.join([text_file, 'is not reachable!']))
            continue
        try:
            if not channel.restricted:
                print(' '.join(['Getting channel', ''.join([x for x in channel.title if x.isalpha()])]))
                posts = client(GetHistoryRequest(
                    peer=channel,
                    limit=999999,
                    offset_date=start_date,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0))
                
                try:
                    for chat in posts.chats:
                      for message in client.iter_messages(chat):
                        channel_messages.append(str(message.to_dict()))
                except:
                    with open(text_file, 'w') as f:
                        f.write(';;;\n;;;'.join(channel_messages))
                    f.close()
                    print('encountered error')
                    print(len(channel_messages))
                    
                with open(text_file, 'w') as f:
                    f.write(';;;\n;;;'.join(channel_messages))
                f.close()
                print(' '.join(['done with', text_file]))
            else:
                print('failed')
                continue
        except:
            print('encountered error')
            continue
