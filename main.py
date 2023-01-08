from flask import Flask, request, jsonify, send_from_directory
import json, os, importlib
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

@app.route('/changeToken', methods=['POST'])
def changeToken():
    args = json.loads(request.get_data().decode('utf-8'))

    with open('.env', 'w', encoding='utf-8') as f:
        f.write(f'TOKEN={args["TOKEN"]}')

    return jsonify({ 'a': True })

@app.route('/addCommand', methods=['POST'])
def addCommand():
    args = json.loads(request.get_data().decode('utf-8'))

    with open(f'./commands/{args["commandName"]}.py', 'w', encoding='utf-8') as f:
        f.write(f'description = "{args["description"]}"\nresponse = "{args["response"]}"\n\nasync def {args["commandName"]}(ctx):\n\tawait ctx.respond(response)')

    return jsonify({ 'a': True })

@app.route('/getCommands', methods=['GET'])
def getCommands():
    commandList = []

    for i in list(filter(lambda x: x.endswith('.py'), os.listdir('./commands'))):
        name = i[:-3]
        
        dt = importlib.import_module(f'commands.{name}')

        jsonData = {}

        jsonData['description'] = dt.description
        jsonData['commandName'] = name
        jsonData['response'] = dt.response

        commandList.append(jsonData)

    return jsonify(commandList)

@app.route('/removeCommand', methods=['POST'])
def removeCommand():
    args = json.loads(request.get_data().decode('utf-8'))

    commandList = []

    for i in list(filter(lambda x: x.endswith('.py'), os.listdir('./commands'))):
        name = i[:-3]
        commandList.append(name)

    if args['commandName'] not in commandList:
        return jsonify({ 'error': 'Command Not Found!' })
    else:
        os.remove(f'./commands/{args["commandName"]}.py')

    return jsonify({ 'code': 'success' })

if __name__ == '__main__':
<<<<<<< HEAD
    t1 = Thread(target=bot.run, args=(os.getenv('TOKEN'), ))
    t2 = Thread(target=app.run, kwargs={'host': '127.0.0.1', 'port': 5000, 'debug': True})

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    # IDEA: wsgi
=======
    app.run(host='127.0.0.1', port=5000, debug=True)
>>>>>>> 6eda54ae01a124990075d21c91cccb3f3c2f86b4
