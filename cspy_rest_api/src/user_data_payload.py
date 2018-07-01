class UserDataPayload:

    def __init__(self, payload):
        self.is_valid = False

        self.steamid = 0
        self.start = 0
        self.end = 0
        self.round_count = 0
        self.map_name = ''

        self.rating1 = 0
        self.hsr, self.ct_hsr, self.t_hsr = 0, 0, 0
        self.mdc, self.ct_mdc, self.t_mdc = 0, 0, 0
        self.kpr, self.ct_kpr, self.t_kpr = 0, 0, 0
        self.kas, self.ct_kas, self.t_kas = 0, 0, 0
        self.kdr, self.ct_kdr, self.t_kdr = 0, 0, 0
        self.kda, self.ct_kda, self.t_kda = 0, 0, 0
        self.mean_equip, self.ct_mean_equip, self.t_mean_equip = 0, 0, 0

        self.load_from_json(payload)

    def get_properties_list(self):
        return [x for x in dir(self) if not x.startswith('__') and x != 'is_valid' and not callable(getattr(self, x))]

    def load_from_json(self, payload):
        try:
            for prop in self.get_properties_list():
                self.__setattr__(prop, payload[prop])
            self.is_valid = True
        except (ValueError, AttributeError, TypeError):
            self.is_valid = False
