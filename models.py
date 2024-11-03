import uuid

class Pilot:
    def __init__(self, name, alts=None):
        self.name = name
        self.alts = alts if alts is not None else []

    def add_alt(self, alt):
        self.alts.append(alt)

class Site:
    PAYOUT_VALUES = {
        -10: 556998042,
        -9: 445598434,
        -8: 356478747,
        -7: 338657810,
        -6: 321722071,
        -5: 305635968,
        -4: 290354172,
        -3: 275836464,
        -2: 262044640,
        -1: 248942410,
        0: 236495287,
        1: 189196231,
        2: 151356986,
        3: 121085589,
        4: 96868472,
        5: 77494779,
        6: 61995823,
        7: 49596658,
        8: 39688328,
        9: 32000000,
        10: 28528500,

    }

    def __init__(self, fleet_pilots, payout=0):
        self.id = uuid.uuid4()
        self.fleet_pilots = fleet_pilots
        self.payout = payout# the +/- of the number of people
        self.site_payout = self.calculate_total_payout()

    def calculate_total_payout(self):
        return self.PAYOUT_VALUES[self.payout] * (self.payout + 15)