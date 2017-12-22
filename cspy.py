# Based on this template: https://github.com/tsuriga/csgo-gsi-qsguide/blob/master/quickstartguide.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime
from logiPy.logiPy import logi_led

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
        self.player_mvps = None
        self.player_score = None
        self.dup_remover = True


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
        status = self.check_status(payload)
        if status == 1:
            self.get_round_info(payload)

            print('game is currently going on.')
            print('current date: %s' % self.server.time)
            print('current name of map: %s' % self.server.map_name)
            print('player name: %s' % self.server.player_name)
            print('what round is it? %s' % self.server.map_round)
            print('the player is on the %s side.' % self.server.player_team)
            print('the %s side won the round.' % self.server.round_winner)
            print('player killed %s enemies this past round.' % self.server.player_round_kills)
            print('player killed %s enemies with headshots this past round.' % self.server.player_round_hs)
            print('\n')
        else:
            if status == 2:
                if self.server.dup_remover:
                    self.server.dup_remover = False
                else:
                    self.get_overall_stats(payload)

                    print('game has ended.')
                    print('current date: %s' % self.server.time)
                    print('current name of map: %s' % self.server.map_name)
                    print('player name: %s' % self.server.player_name)
                    print('player total kills: %s' % self.server.player_kills)
                    print('player total deaths: %s' % self.server.player_deaths)
                    print('player total assists: %s' % self.server.player_assists)
                    print('player score: %s' % self.server.player_score)
                    print('# of mvps: %s' % self.server.player_mvps)
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
                                return 1

            if map_phase == 'gameover':  # if match is over, indicate as such, in order to collect match stats.
                if payload['player']['match_stats']['score'] != self.server.player_score:
                    return 2
        return 0

    # individual round data
    def get_round_info(self, payload):
        if 'map' in payload:
            if 'name' in payload['map']:  # get map name
                self.server.map_name = payload['map']['name']

            if 'round' in payload['map']:  # get round number
                self.server.map_round = payload['map']['round']

        if 'player' in payload:
            if 'name' in payload['player']:  # get player name
                self.server.player_name = payload['player']['name']

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

        if 'provider' in payload and 'timestamp' in payload['provider']:  # get time of game
            time = datetime.utcfromtimestamp(payload['provider']['timestamp'])
            format_time = str(time.strftime('%b %d, %Y'))
            self.server.time = format_time

    # overall match data
    def get_overall_stats(self, payload):
        if 'map' in payload:
            if 'name' in payload['map']:  # get map name
                self.server.map_name = payload['map']['name']

        if 'player' in payload:

            if 'name' in payload['player']:  # get player name
                self.server.player_name = payload['player']['name']

            if 'match_stats' in payload['player']:  # get player's match stats
                if 'kills' in payload['player']['match_stats']:
                    self.server.player_kills = payload['player']['match_stats']['kills']

                if 'assists' in payload['player']['match_stats']:
                    self.server.player_assists = payload['player']['match_stats']['assists']

                if 'deaths' in payload['player']['match_stats']:
                    self.server.player_deaths = payload['player']['match_stats']['deaths']

                if 'mvps' in payload['player']['match_stats']:
                    self.server.player_mvps = payload['player']['match_stats']['mvps']

                if 'score' in payload['player']['match_stats']:
                    self.server.player_score = payload['player']['match_stats']['score']

        if 'provider' in payload and 'timestamp' in payload['provider']:  # get time of game
            time = datetime.utcfromtimestamp(payload['provider']['timestamp'])
            format_time = str(time.strftime('%b %d, %Y'))
            self.server.time = format_time

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
