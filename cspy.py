# Based on this template: https://github.com/tsuriga/csgo-gsi-qsguide/blob/master/quickstartguide.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime


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
        self.player_kills = None
        self.player_assists = None
        self.player_deaths = None


class GSRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode('utf-8')

        self.main_payload(json.loads(data))

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    def main_payload(self, payload):
        if self.check_status(payload):
            self.get_round_info(payload)

            print(self.server.map_round)
            print(self.server.player_team)
            print(self.server.round_winner)
            print(self.server.player_round_kills)
            print(self.server.player_round_hs)
            print('\n\n')

    def check_status(self, payload):
        if 'map' in payload and 'phase' in payload['map']:
            map_phase = payload['map']['phase']
            if map_phase == 'live':
                if 'round' in payload and 'phase' in payload['round']:
                    round_phase = payload['round']['phase']
                    if round_phase == 'over':
                        return True

        return False

    def get_round_info(self, payload):
        if 'map' in payload:
            if 'round' in payload['map']:  # get round number
                self.server.map_round = payload['map']['round']

        if 'player_id' in payload:
            if 'team' in payload['player_id']:  # get which side player is on
                self.server.player_team = payload['player_id']['team']

        if 'round' in payload:
            if 'win_team' in payload['round']:  # get winning team
                self.server.round_winner = payload['round']['win_team']

        if 'player_state' in payload:  # get player stats for the past round
            if 'player' in payload['player_state']:
                if 'state' in payload['player_state']['player']:
                    if 'round_kills' in payload['player_state']['player']['state']:
                        self.server.player_round_kills = payload['player_state']['player']['state']['round_kills']

                    if 'round_killhs' in payload['player_state']['player']['state']:
                        self.server.player_round_hs = payload['player_state']['player']['state']['round_killhs']

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

    # using round_phase and round_winner, get player stats per round:
    # player_team, player_round_kills, player_round_hs
    def get_round_info(self, payload):
        pass

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
