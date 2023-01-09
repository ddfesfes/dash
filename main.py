from flask import Flask, request, jsonify, send_from_directory
import json, os, importlib, re
from threading import Thread

app = Flask(__name__)

import discord
from dotenv import load_dotenv

from threading import Thread

# bot = discord.Bot()

load_dotenv()
bot = discord.Bot()

@bot.listen()
async def on_ready():
    print('ready')

for i in list(filter(lambda x: x.endswith('.py'), os.listdir('./commands'))):
    name = i[:-3]

    dt = importlib.import_module(f'commands.{name}')
    func = eval(f'dt.{name}')
    bot.command(description=dt.description)(func)

@app.route("/")
def main():
    return send_from_directory('client/dist', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/dist', path)

@app.route('/token', methods=['GET', 'POST'])
def token():
    if request.method == 'POST':
        args = json.loads(request.get_data().decode('utf-8'))

        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f'TOKEN={args["TOKEN"]}')

        return jsonify({ 'a': True })

    elif request.method == 'GET':
        with open('.env', 'r', encoding='utf-8') as f:
            data = re.sub('TOKEN=(.*)', '$1', f.read())

        return jsonify({ 'token': data })

@app.route('/command', methods=['GET', 'POST'])
def commands():
    if request.method == 'GET':
        commandList = []

        for i in list(filter(lambda x: x.endswith('.py'), os.listdir('./commands'))):
            name = i[:-3]
            jsonData = {}
            jsonData['commandName'] = name
            
            commandList.append(jsonData)

        return jsonify(commandList)
    elif request.method == 'POST':
        args = json.loads(request.get_data().decode('utf-8'))

        with open(f'./commands/{args["commandName"]}.py', 'w', encoding='utf-8') as f:
            f.write(f'description = "{args["description"]}"\nresponse = "{args["response"]}"\n\nasync def {args["commandName"]}(ctx):\n\tawait ctx.respond(response)')

        return jsonify({ 'a': True })

@app.route('/command/<commandName>', methods=['GET', 'REMOVE'])
def command(commandName):
    if request.method == 'GET':
        commandList = []
        com = []

        for i in list(filter(lambda x: x.endswith('.py'), os.listdir('./commands'))):
            name = i[:-3]
            commandList.append(name)
        
        if commandName in commandList:
            dt = importlib.import_module(f'commands.{commandName}')

            jsonData = {}

            jsonData['description'] = dt.description
            jsonData['commandName'] = commandName
            jsonData['response'] = dt.response

            com.append(jsonData)
        
        return jsonify(com)

    elif request.method == 'REMOVE':
        commandList = []

        for i in list(filter(lambda x: x.endswith('.py'), os.listdir('./commands'))):
            name = i[:-3]
            commandList.append(name)

        if commandName not in commandList:
            return jsonify({ 'error': 'Command Not Found!' })
        else:
            os.remove(f'./commands/{commandName}.py')

        return jsonify({ 'code': 'success' })

if __name__ == '__main__':
    # t1 = Thread(target=bot.run, args=(os.getenv('TOKEN'), ))
    t2 = Thread(target=app.run, kwargs={'host': '127.0.0.1', 'port': 5000, 'debug': True})

    # t1.start()
    t2.start()

    # t1.join()
    t2.join()