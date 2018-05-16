from enum import Enum

class GameStateCode(Enum):
    INVALID = -1
    ENDGAME = 0
    VALID = 1

def get_properties_list(obj):
    return [x for x in dir(obj) if not x.startswith('__') and not callable(getattr(obj, x))]

def load_nested_data(root_payload):
    for prop in get_properties_list(root_payload):
        if type(root_payload.__getattribute__(prop)) is dict:
            subsection = Payload(root_payload.__getattribute__(prop))
            root_payload.__setattr__(prop, subsection)
            load_nested_data(subsection)

class Payload(object):

    def __init__(self, payload):
        self.__dict__ = payload
        load_nested_data(self)

    # KEY PROPERTIES
    #
    # provider.timestamp
    # map.name
    # map.phase
    # player.name
    # player.team
    # player.match_stats
    # player.state
    #
    # PROPERTIES FOR CHECKS
    # player.activity
    # map.mode
    # map.round
    # provider.steamid
    # player.steamid
    # round.phase
    # previously.player.state
    # previously.round.phase

    # check the existence of key properties (provider, player, map, etc)
    def basic_check(self):


    # check which category of payload this is
    def classify_payload(self):



    # def check_payload(self):
    #     try:
    #         if self.player['activity'] == 'playing' and self.map['mode'] == 'competitive':
    #             map_phase = self.map['phase']
    #             if map_phase == 'live' or map_phase == 'intermission' or map_phase == 'gameover':
    #                 round_phase = self.round['phase']
    #                 prev_round_phase = self.previous['round']['phase']
    #                 user_id = self.client['steamid']
    #                 curr_player_id = self.player['steamid']
    #
    #                 if user_id == curr_player_id:
    #                     if round_phase == 'over' and prev_round_phase == 'live':
    #                         print('valid, end-round data')
    #                         return GameStateCode.VALID
    #                     elif (round_phase == 'live' and self.player['state']['health'] == 0
    #                           and self.previous['player']['state']['health'] > 0):
    #                         print('valid, mid-round data')
    #                         return GameStateCode.VALID
    #
    #                 else:
    #                     if (map_phase == 'gameover' and round_phase == 'over'
    #                         and prev_round_phase == 'live'):
    #                         print('endgame data')
    #                         return GameStateCode.ENDGAME
    #
    #         print('invalid data')
    #         return GameStateCode.INVALID
    #     except(TypeError, ValueError, KeyError):
    #         print('invalid data')
    #         return GameStateCode.INVALID
    #
    #
    # def insert_data_to_db(self, player_db):
    #     if self.gamestate_code == GameStateCode.VALID:
    #         player_team = None if 'team' not in self.player else self.player['team']
    #         match_stats = self.player['match_stats']
    #         player_state = self.player['state']
    #
    #         new_player_data = (int(self.client['timestamp']),
    #                              self.map['name'], self.map['phase'],
    #                              self.player['name'], player_team,
    #                              int(match_stats['kills']),
    #                              int(match_stats['assists']),
    #                              int(match_stats['deaths']),
    #                              int(match_stats['mvps']),
    #                              int(match_stats['score']),
    #                              int(player_state['equip_value']),
    #                              int(player_state['round_kills']),
    #                              int(player_state['round_killhs']))
    #
    #         sql_insert = ''' INSERT INTO per_round_data(Time, Map, "Map Status", "Player Name", "Player Team",
    #                                                     Kills, Assists, Deaths, MVPs, Score, "Current Equip. Value",
    #                                                     "Round Kills", "Round HS Kills")
    #                                                     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    #     else:
    #         new_player_data = (int(self.client['timestamp']), self.map['name'], self.map['phase'])
    #
    #         sql_insert = ''' INSERT INTO per_round_data(Time, Map, "Map Status") VALUES(?, ?, ?) '''
    #
    #     player_db.cursor().execute(sql_insert, new_player_data)