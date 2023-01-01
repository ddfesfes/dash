import discord
import os, time
from dotenv import load_dotenv
import importlib

from threading import Thread

load_dotenv()
bot = discord.Bot()

for i in list(filter(lambda x: x.endswith('.py'), os.listdir('./commands'))):
    name = i[:-3]

    dt = importlib.import_module(f'commands.{name}')
    func = eval(f'dt.{name}')
    bot.command(description=dt.description)(func)

@bot.listen()
async def on_ready():
    print('ready')

def check():
    latest = len(os.listdir('./commands'))

    while True:
        data = len(os.listdir('./commands'))

        if data != latest:
            print('파일 변경됨 리로드 ㄱㄱ')

        latest = data

        time.sleep(0.3)

if __name__ == '__main__':
    t1 = Thread(target=bot.run, args=(os.getenv('TOKEN'), ))
    t2 = Thread(target=check)

    t1.start()
    t2.start()

    t1.join()
    t2.join()