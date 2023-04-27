from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False,
        }
    }
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


AGREEMENTS = ['ладно', 'куплю', 'покупаю', 'хорошо']
DISAGREEMENTS = ["не хочу", "не буду", "отстань!"]


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        sessionStorage[user_id] = {'suggests': DISAGREEMENTS}
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() in AGREEMENTS:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return
    res['response']['text'] = f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]
    suggests = [{'title': suggest, 'hide': True} for suggest in session['suggests'][:2]]
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session
    if len(suggests) < 2:
        suggests.append({"title": "Ладно", "url": "https://market.yandex.ru/search?text=слон", "hide": True})
    return suggests


if __name__ == '__main__':
    app.run()

# https://dialogs.yandex.ru/developer/skills/8760c5bf-cf8b-49d5-804a-9dccd324d5d8/draft/test

# test.py

# import requests
# import json
#
# data = json.loads('''{
#                         "request": {
#                             "command": "закажи пиццу на улицу льва толстого, 16 на завтра",
#                             "original_utterance": "закажи пиццу на улицу льва толстого, 16 на завтра"
#                         },
#                         "session": {
#                             "new": true,
#                             "message_id": 4,
#                             "session_id": "2eac4854-fce721f3-b845abba-20d60",
#                             "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
#                             "user_id": "AC9WC3DF6FCE052E45A4566A48E6B7193774B84814CE49A922E163B8B29881DC"
#                         },
#                         "version": "1.0"
#                     }''')
#
# res = requests.port("https://localhost:5000/port", json=data)
#
# print(res.json())
