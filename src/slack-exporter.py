#!/usr/bin/python3

import json
import os

from slackclient import SlackClient

client = SlackClient(token=os.environ['SLACK_API_TOKEN'])


def has_true_value(dict_obj, key):
    return key in dict_obj and dict_obj[key]


def print_json(dict_obj):
    print(json.dumps(
        dict_obj,
        sort_keys=True,
        indent=2,
        separators=(',', ': ')
    ))


def check_response_ok(response):
    if not response['ok']:
        raise Exception('Slack API call failed, error: %s' % str(response))


def get_conversation_info(channel_id):
    response = client.api_call(
        'conversations.info',
        channel=channel_id,
        include_locale=True,
        include_num_members=True
    )

    check_response_ok(response)

    channel = response['channel']

    if has_true_value(channel, 'is_archived') or \
            ('num_members' in channel and channel['num_members'] == 0):
        channel['members'] = []
    else:
        rsp_members = client.api_call(
            'conversations.members',
            channel=channel_id,
            limit=1000
        )

        check_response_ok(rsp_members)

        channel['members'] = rsp_members['members']

    return channel


def get_conversation_history(channel_id):
    all_messages = []
    has_more = True
    cursor = None
    while has_more:
        if cursor:
            response = client.api_call(
                'conversations.history',
                channel=channel_id,
                limit=1000,
                cursor=cursor
            )
        else:
            response = client.api_call(
                'conversations.history',
                channel=channel_id,
                limit=1000
            )

        check_response_ok(response)

        has_more = False
        if 'response_metadata' in response and \
                'next_cursor' in response['response_metadata']:
            cursor = response['response_metadata']['next_cursor']
            has_more = True

        all_messages.extend(response['messages'])

    return all_messages


def get_users():
    response = client.api_call(
        'users.list',
        limit=1000
    )

    check_response_ok(response)

    members = response['members']
    print('Got %d members' % len(members))

    return members


def save_json(out_dir, out_file_name, data):
    os.makedirs(out_dir, exist_ok=True)

    file_path = os.path.join(out_dir, out_file_name)

    with open(file_path, "w", encoding='utf-8') as f_obj:
        json.dump(data,
                  f_obj, ensure_ascii=False,
                  sort_keys=True,
                  indent=2,
                  separators=(',', ': '))


def get_conversations(out_dir, refresh=False):
    response = client.api_call(
        'conversations.list',
        types='public_channel, private_channel, mpim, im',
        limit=1000
    )

    check_response_ok(response)

    channels = response['channels']
    print('Got %d channels' % len(channels))

    all_channels = []
    all_mpims = []
    all_ims = []
    all_groups = []
    for channel in channels:
        save_name = ''
        out_dir_prefix = ''
        if has_true_value(channel, 'is_channel'):
            save_name = channel['name']
            print('Channel name: %s' % channel['name'])
        elif has_true_value(channel, 'is_private'):
            save_name = channel['name']
            print('Private channel name: %s' % channel['name'])
        elif has_true_value(channel, 'is_im'):
            save_name = channel['id']
            print('DM id: %s' % channel['id'])

        channel_info = get_conversation_info(channel['id'])

        if has_true_value(channel, 'is_mpim'):
            all_mpims.append(channel_info)
        elif has_true_value(channel, 'is_im'):
            all_ims.append(channel_info)
        elif has_true_value(channel, 'is_group'):
            all_groups.append(channel_info)
        else:
            all_channels.append(channel_info)

        messages_file_name = save_name + '-messages.json'
        messages_file_path = os.path.join(out_dir, save_name, messages_file_name)

        if refresh or not os.path.exists(messages_file_path):
            messages = get_conversation_history(channel['id'])
            save_json(os.path.join(out_dir, save_name),
                      messages_file_name,
                      messages)

    save_json(out_dir, 'channels.json', all_channels)
    save_json(out_dir, 'mpims.json', all_mpims)
    save_json(out_dir, 'dms.json', all_ims)
    save_json(out_dir, 'groups.json', all_groups)

    users = get_users()
    save_json(out_dir, 'users.json', users)


if __name__ == '__main__':
    get_conversations('../exported', False)
