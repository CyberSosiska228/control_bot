import subprocess
import telebot
import time
import signal
import os

f = open("token", "r")
token = f.readlines()[0][:-1]
f.close()

f = open("users", "r")
users = []
for i in f.readlines():
    users.append(int(i))
f.close()

bot = telebot.TeleBot(token)
max_execution_time = 3


def run(message):
    res = subprocess.check_output(message.text[9:], shell=True).decode()
    for i in range(0, len(res), 4096):
        bot.send_message(message.from_user.id, res[i : min(i + 4096, len(res))])
    exit(0)


def check(message):
    if (len(users) == 0 or message.from_user.id in users):
        return True
    return False

def execute(message):
    if (not check(message)):
        bot.send_message(message.from_user.id, "You are not allowed to use this bot")
        return

    pid_0 = os.fork()
    if (not pid_0):
        pid_1 = os.fork()
        if (pid_1):
            time.sleep(max_execution_time)
            os.kill(pid_1, signal.SIGUSR1)
        else:
            run(message)
        exit(0)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if (message.text[:9] == "/execute "):
        execute(message)

while True:
    bot.polling(none_stop=True, interval=0)
    continue
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        time.sleep(60)
