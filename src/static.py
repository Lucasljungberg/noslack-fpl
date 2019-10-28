import json
from collections import namedtuple


PLPlayerPosition = namedtuple('PlayerPosition', ['name', 'shortname'])
PLTeam = namedtuple('PLTeam', ['name', 'shortname'])

with open('test-files/static-fpl-info.json', 'r') as f:
    data = json.loads(f.read())

POSITION_ID = {
    1: PLPlayerPosition('Goalkeeper', 'GKP'),
    2: PLPlayerPosition('Defender', 'DEF'),
    3: PLPlayerPosition('Midfielder', 'MID'),
    4: PLPlayerPosition('Forward', 'FWD'),
}
PLTEAM_ID = {
    1: PLTeam('Arsenal', 'ARS'),
    2: PLTeam('Aston Villa', 'AVL'),
    3: PLTeam('Bournemouth', 'BOU'),
    4: PLTeam('Brighton', 'BHA'),
    5: PLTeam('Burnley', 'BUR'),
    6: PLTeam('Chelsea', 'CHE'),
    7: PLTeam('Crystal Palace', 'CRY'),
    8: PLTeam('Everton', 'EVE'),
    9: PLTeam('Leicester', 'LEI'),
    10: PLTeam('Liverpool', 'LIV'),
    11: PLTeam('Man City', 'MCI'),
    12: PLTeam('Man Utd', 'MUN'),
    13: PLTeam('Newcastle', 'NEW'),
    14: PLTeam('Norwich', 'NOR'),
    15: PLTeam('Sheffield Utd', 'SHU'),
    16: PLTeam('Southampton', 'SOU'),
    17: PLTeam('Spurs', 'TOT'),
    18: PLTeam('Watford', 'WAT'),
    19: PLTeam('West Ham', 'WHU'),
    20: PLTeam('Wolves', 'WOL'),
}

class PLPlayer:
    def __init__(self, pid, name, role_id, team_id):
        self.pid = pid
        self.name = name
        self.role_id = role_id
        self.team_id = team_id

    @classmethod
    def from_api(cls, id, web_name, element_type, team, *args, **kw):
        return cls(pid=id,
                   name=web_name,
                   role_id=element_type,
                   team_id=team)

    @property
    def role(self):
        return POSITION_ID[self.role_id]

    @property
    def plteam(self):
        return PLTEAM_ID[self.team_id]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'{self.__class__.__qualname__}(id={self.pid}, '
                f"name='{self.name}', "
                f'{self.plteam}, '
                f'{self.role})')

players = {}
for api_player_data in data['elements']:
    player = PLPlayer.from_api(**api_player_data)
    players[player.pid] = player


