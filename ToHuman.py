from datetime import datetime
import re
import sys


def get_chat_dataframe(file):
    data = []

    with open('human-log.txt', 'w'):
        pass
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n\n\n')

        for line in lines:
            try:
                time_logged = line.split('—')[0].strip()
                time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')

                username_message = line.split('—')[1:]
                username_message = '—'.join(username_message)

                username, channel, message = re.search(
                    ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', username_message
                ).groups()

                d = {
                    'dt': time_logged,
                    'channel': channel,
                    'username': username,
                    'message': message
                }

                original_stdout = sys.stdout

                with open('human-log.txt', 'a') as f:
                    sys.stdout = f
                    print(f'{d["dt"]}\t{d["channel"]}\t{d["username"]}\t{d["message"]}')
                    sys.stdout = original_stdout

                data.append(d)

            except Exception:
                pass


get_chat_dataframe('chat.log')
