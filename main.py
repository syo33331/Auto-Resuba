import requests
import datugokun

base = 'https://discord.com/api/v8'

Channel_id = 'botが会話するチャンネルID'
token = 'あなたのトークン' 
bot_user_id = 'あなたのUserID'  

HEADERS = {
    'Authorization': token,
    'Content-Type': 'application/json',
}

def get_latest_message(channel_id):
    url = f'{base}/channels/{channel_id}/messages?limit=1'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        messages = response.json()
        return messages[0] if messages else None
    return None

def send_message(channel_id, message, reference_message_id):
    url = f'{base}/channels/{channel_id}/messages'
    data = {
        'content': message,
        'message_reference': {'message_id': reference_message_id}
    }
    response = requests.post(url, headers=HEADERS, json=data)
    return response.status_code == 200

def main():
    channel_id = Channel_id
    replied_messages = set()
    while True:
        latest_message = get_latest_message(channel_id)
        if latest_message and latest_message['id'] not in replied_messages:
            if latest_message['author']['id'] != bot_user_id:
                question = datugokun.question(latest_message['content'])
                if send_message(channel_id, question, latest_message['id']):
                    replied_messages.add(latest_message['id'])

if __name__ == '__main__':
    main()
