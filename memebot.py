from slackclient import SlackClient
import time, io, os
from addtext import add_text, OutputFile
from memelist import meme_images
from customresponses import phrases

SLACK_BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_ID = os.environ['BOT_ID']
AT_BOT = '<@{}>'.format(BOT_ID)
sc = SlackClient(SLACK_BOT_TOKEN)

def main_loop(refresh_interval=1):
    while True:
        message, channel = parse_output(sc.rtm_read())
        if message and channel:
            respond(handle_message(message), channel)
        time.sleep(refresh_interval)

def parse_output(rtm_output):
    for output in rtm_output:
        if 'user' in output and output['user'] != BOT_ID and 'text' in output:
            return output['text'], output['channel']
    return None, None

def handle_message(message):
    if AT_BOT in message:
        return directly_invoked(message.split(AT_BOT)[1])
    try:
        return phrases[message.lower()]()
    except KeyError:
        return None

def respond(response, channel):
    if type(response) is OutputFile:
        sc.api_call('files.upload', file=response.file.getvalue(), filename='meme.{}'.format(response.filetype), channels=channel, as_user=True)
    elif type(response) is str:
        sc.api_call('chat.postMessage', channel=channel, text=response, as_user=True)

def directly_invoked(message):
    split_message = message.split()
    if len(split_message) == 0:
        return None
    if split_message[0] == 'help':
        return help_message()
    if len(split_message) > 1:
        meme_type = split_message[0]
        text = ' '.join(split_message[1:]).replace('\\n', '\n')
        return add_text(meme_type, text)
    return None

def help_message():
    return 'I am versed in the following memes: {}'.format(', '.join(meme_images))

if __name__ == '__main__':
    if sc.rtm_connect():
        print('I\'m alive!')
        main_loop()
    else:
        print('Connection failed...')
