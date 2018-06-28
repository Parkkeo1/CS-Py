from enum import Enum


class GameStateCode(Enum):
    INVALID = -1
    ENDGAME_DIFF_PLAYER = 0
    VALID = 1


class GameStatePayload:

    def __init__(self, payload):
        self.__dict__ = payload
        self.load_nested_data()
        # TODO: Track client's steamID as attribute. Add new field to per_round_data table. Then in MatchDataSummary,
        # TODO: add attribute to client SteamID. This attribute will be used in the JSON POST Request to the remote server
        # TODO: (probably headers, if not in the content of JSON).

        self.gamestate_code = self.classify_payload()

    def get_properties_list(self):
        return [x for x in dir(self) if not x.startswith('__') and not callable(getattr(self, x))]

    def load_nested_data(self):
        for prop in self.get_properties_list():
            if type(self.__getattribute__(prop)) is dict:
                subsection = GameStatePayload(self.__getattribute__(prop))
                self.__setattr__(prop, subsection)
                subsection.load_nested_data()

    # KEY PROPERTIES            PROPERTIES FOR CHECKS
    #
    # provider.timestamp        player.activity
    # map.name                  map.mode
    # map.phase                 map.round
    # player.name               provider.steamid
    # player.team               player.steamid
    # player.match_stats        round.phase
    # player.state              previously.player.state
    #                           previously.round.phase

    # check the existence of key properties (provider, player, map, etc)
    def basic_check(self):
        try:
            print("Pass #1: {0}, {1}, {2}, {3}, {4}, {5}".format(self.provider.timestamp, self.map.name, self.map.phase,
                                                                 self.player.name, self.player.team, self.player.match_stats,
                                                                 self.player.state))
            print("Pass #2: {0}, {1}, {2}, {3}, {4}, {5}".format(self.player.activity, self.map.mode, self.map.round,
                                                                 self.provider.steamid, self.player.steamid,
                                                                 self.round.phase))
            return True
        except (TypeError, AttributeError, ValueError):
            return False

    valid_map_phases = {'live', 'intermission', 'gameover'}

    # check which category of payload this is
    def classify_payload(self):
        if not self.basic_check():
            return GameStateCode.INVALID
        elif self.player.activity == 'playing' and self.map.mode == 'competitive':
            if self.map.phase in GameStatePayload.valid_map_phases:

                if self.provider.steamid == self.player.steamid:  # if player is alive (not an observer at time of payload)
                    if self.round.phase == 'over':  # end-of-round, player is alive
                        try:
                            return GameStateCode.VALID if self.previously.round.phase == 'live' else GameStateCode.INVALID

                        except (TypeError, AttributeError, ValueError):
                            return GameStateCode.INVALID
                    elif self.round.phase == 'live' and self.player.state.health == 0:  # mid-round, player dies
                        try:
                            return GameStateCode.VALID if self.previously.player.state.health > 0 else GameStateCode.INVALID

                        except (TypeError, AttributeError, ValueError):
                            return GameStateCode.INVALID
                else:
                    if self.map.phase == 'gameover' and self.round.phase == 'over':  # end-game
                        try:
                            return GameStateCode.ENDGAME_DIFF_PLAYER if self.previously.round.phase == 'live' else GameStateCode.INVALID

                        except (TypeError, AttributeError, ValueError):
                            return GameStateCode.INVALID

        return GameStateCode.INVALID
