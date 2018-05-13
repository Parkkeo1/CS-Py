from enum import Enum

class GameStateCode(Enum):
    INVALID = -1
    ENDGAME = 0
    VALID = 1

class Payload:

    def __init__(self, payload):
        self.map = payload['map']
        self.player = payload['player']
        self.client = payload['provider']
        self.round = payload['round']
        self.previous = payload['previously']

        self.gamestate_code = self.check_payload()

    def check_payload(self):
        try:
            if self.player['activity'] == 'playing' and self.map['mode'] == 'competitive':
                map_phase = self.map['phase']
                if map_phase == 'live' or map_phase == 'intermission' or map_phase == 'gameover':
                    round_phase = self.round['phase']
                    prev_round_phase = self.previous['round']['phase']
                    user_id = self.client['steamid']
                    curr_player_id = self.player['steamid']


                    if user_id == curr_player_id:
                        if round_phase == 'over' and prev_round_phase == 'live':
                            return GameStateCode.VALID
                        elif (round_phase == 'live' and self.player['state']['health'] == 0
                              and self.previous['player']['state']['health'] > 0):
                            return GameStateCode.VALID

                    else:
                        if (map_phase == 'gameover' and round_phase == 'over'
                            and prev_round_phase == 'live'):
                            return GameStateCode.ENDGAME

            return GameStateCode.INVALID
        except(TypeError, ValueError):
            return GameStateCode.INVALID



