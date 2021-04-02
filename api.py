from flask import Flask, request
import logging
import json
import random
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

class QuakeReq():
    def __init__(self, name):
        qc_req = requests.get(f'https://quake-stats.bethesda.net/api/v2/Player/Stats?name={name}')
        if qc_req.status_code == 500:
            self.status_code = 500
        else:
            self.status_code = 200
            self.name = qc_req.json()['name']

            self.duel = qc_req.json()["playerRatings"]["duel"]
            self.duel_rating = self.duel['rating']
            self.duel_deviation = self.duel["deviation"]
            self.duel_gamescount = self.duel["gamesCount"]
            self.duel_last_update = self.duel['lastChange']

            self.tdm = qc_req.json()["playerRatings"]["tdm"]
            self.tdm_rating = self.tdm['rating']
            self.tdm_deviation = self.tdm["deviation"]
            self.tdm_gamescount = self.tdm["gamesCount"]
            self.tdm_last_update = self.tdm['lastChange']

    def full_info(self):
        if self.status_code == 500:
            print('Invalid nickname, try another one')
        else:
            return (f'Name: {self.name}\n \n'
                    f'Duel: {self.duel_rating}±{self.duel_deviation} (Games: {self.duel_gamescount})\n'
                    f'2v2 TDM: {self.tdm_rating}±{self.duel_deviation} (Games: {self.tdm_gamescount})')


@app.route('/', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Hi! Thats Quake Stats Checker. Print Nickname'
        return

    else:
        for entity in req['request']['nlu']['tokens']:
            print(entity)
            name = entity
        qcreq = QuakeReq(name)
        qcinf = qcreq.full_info()
        res['response']['text'] = qcinf

if __name__ == '__main__':
    app.run()