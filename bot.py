#!/usr/bin/env python3

from flask import Flask, request
from webexteamssdk import WebexTeamsAPI, Webhook
import json

ACCESS_TOKEN = 'NDMyNmM5NzYtOTJlNi00ZWMwLThiZDMtMGY0NDNkNjZhMTQ4MjE5MGU1NzYtNmQ3_PF84_4590eb6a-2ca2-4394-bc27-9b671ce2fe73'
WEBHOOK_NAME = 'MyWebook'
PUBLIC_BOT_URL = 'https://df45cc4a.ngrok.io'

app = Flask(__name__)
teams_api = WebexTeamsAPI(access_token=ACCESS_TOKEN)
myId = None

def set_up_webhook():
    for webhook in teams_api.webhooks.list():
        if webhook.name == WEBHOOK_NAME:
            teams_api.webhooks.delete(webhook.id)
    teams_api.webhooks.create(name=WEBHOOK_NAME, targetUrl=PUBLIC_BOT_URL,
                              resource='messages', event='created', filter=None)

@app.route('/', methods=['POST'])
def teamswebhook():
    webhook_obj = Webhook(request.json)
    message_data = webhook_obj.data

    if message_data.personId == myId:
    	return '200'

    email = message_data.personEmail
    message = teams_api.messages.get(message_data.id)
    person = teams_api.people.get(message_data.personId)

    print("FROM '{}'".format(person.displayName))
    print("MESSAGE '{}'\n".format(message.text))

    teams_api.messages.create(toPersonEmail=message_data.personEmail, text='Hello2 ' + person.firstName + ' your message was ' + message.text + ' your email is ' + email)
    return '200'

if __name__ == '__main__':
    myId = teams_api.people.me().id
    set_up_webhook()
    app.run(host='localhost', port=3000)
