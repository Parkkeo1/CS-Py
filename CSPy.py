# Based on this template: https://github.com/tsuriga/csgo-gsi-qsguide/blob/master/quickstartguide.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import json
from datetime import datetime


class InfoServer(HTTPServer):
    def init_state(self):
        self.time = None
        self.map_name = None
        self.map_live = False
        self.map_round = None
        self.round_phase = None
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

        self.parse_payload(json.loads(data))

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    def parse_payload(self, payload):
        self.get_game_info(payload)
        if self.server.map_live:  # check if map is live before collecting stats
            print('new payload info:')
            print(self.server.time)
            print(self.server.map_name)
            print(self.server.map_round)
            print(self.server.player_name)

    # get time, map_name, map_live, map_round, player_name
    def get_game_info(self, payload):
        if 'map' in payload and 'phase' in payload['map']:
            phase = str(payload['map']['phase'])
            if phase == 'live':
                self.server.map_live = True
            else:
                self.server.map_live = False

        if self.server.map_live:
            if 'provider' in payload and 'timestamp' in payload['provider']:
                time = datetime.utcfromtimestamp(payload['provider']['timestamp'])
                format_time = str(time.strftime('%b %d, %Y'))
                self.server.time = format_time

            if 'map' in payload:
                if 'name' in payload['map']:
                    map = str(payload['map']['name'])
                    self.server.map_name = map

                if 'round' in payload['map']:
                    nth_round = payload['map']['round']
                    self.server.map_round = nth_round

            if 'player_id' in payload:
                if 'name' in payload['player_id']:
                    name = str(payload['player_id']['name'])
                    self.server.player_name = name

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
server.init_state()

print('server has started')

try:
    server.serve_forever()
except (KeyboardInterrupt, SystemExit):
    pass

server.server_close()
print('server has stopped')
