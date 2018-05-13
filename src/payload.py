from enum import Enum

class PayloadType(Enum):
    BLANK = -1,
    INVALID = 0,
    VALID = 1,
    ENDGAME = 2

class Payload:

    def __init__(self, json_data):
        self.payload_type = PayloadType.BLANK

