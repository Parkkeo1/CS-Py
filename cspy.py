# Based on this template: https://github.com/tsuriga/csgo-gsi-qsguide/blob/master/quickstartguide.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime
from logiPy.logipy import logi_led


class InfoServer(HTTPServer):
    def start(self):
        self.time = None
        self.map_name = None
        self.map_round = None
        self.round_winner = None
        self.player_name = None
        self.player_team = None
        self.player_round_kills = None
        self.player_round_hs = None


class GSRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        data = json.loads(body)

        self.logi_payload(data)
        self.main_payload(data)

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    def logi_payload(self, payload):  # TODO: Logitech's RGB LED SDK for mice. Testing on G303 and G203.
        pass

    def main_payload(self, payload):
        if self.check_status(payload):
            self.get_round_info(payload)

            print('what round is it? %s' % self.server.map_round)
            print('the player is on the %s side.' % self.server.player_team)
            print('the %s side won the round.' % self.server.round_winner)
            print('player killed %s enemies this past round.' % self.server.player_round_kills)
            print('player killed %s enemies with headshots this past round.' % self.server.player_round_hs)
            print('\n')

    def check_status(self, payload):  # to prevent repetitious data
        if 'map' in payload and 'phase' in payload['map']:
            map_phase = payload['map']['phase']
            if map_phase == 'live':  # make sure map is live
                if 'round' in payload and 'phase' in payload['round']:
                    round_phase = payload['round']['phase']
                    if round_phase == 'over':  # make sure round is over
                        if 'map' in payload and 'round' in payload['map']:
                            number = payload['map']['round']
                            if number != self.server.map_round and number != 0:  # make sure it is a new round
                                return True

        return False

    def get_round_info(self, payload):
        if 'map' in payload:
            if 'round' in payload['map']:  # get round number
                self.server.map_round = payload['map']['round']

        if 'player' in payload:
            if 'team' in payload['player']:  # get which side player is on
                self.server.player_team = payload['player']['team']

            if 'state' in payload['player']:  # get player stats for the past round
                if 'round_kills' in payload['player']['state']:
                    self.server.player_round_kills = payload['player']['state']['round_kills']

                if 'round_killhs' in payload['player']['state']:
                    self.server.player_round_hs = payload['player']['state']['round_killhs']

        if 'round' in payload:
            if 'win_team' in payload['round']:  # get winning team
                self.server.round_winner = payload['round']['win_team']

    # # get time, map_name, map_round, player_name
    # def get_game_info(self, payload):
    #     if 'provider' in payload and 'timestamp' in payload['provider']:
    #         time = datetime.utcfromtimestamp(payload['provider']['timestamp'])
    #         format_time = str(time.strftime('%b %d, %Y'))
    #         self.server.time = format_time
    #
    #     if 'map' in payload:
    #         if 'name' in payload['map']:
    #             map = str(payload['map']['name'])
    #             self.server.map_name = map
    #
    #         if 'round' in payload['map']:
    #             nth_round = payload['map']['round']
    #             self.server.map_round = nth_round
    #
    #     if 'player_id' in payload:
    #         if 'name' in payload['player_id']:
    #             name = str(payload['player_id']['name'])
    #             self.server.player_name = name

    # get overall player stats for the entire map/game: kills, assists, deaths
    def get_overall_stats(self, payload):
        pass

    def log_message(self, format, *args):
        return


server = InfoServer(('localhost', 3000), GSRequestHandler)
server.start()

print('server has started')

try:
    server.serve_forever()
except (KeyboardInterrupt, SystemExit):
    pass

server.server_close()
print('server has stopped')
