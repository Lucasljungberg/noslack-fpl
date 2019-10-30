import datetime
import json
from collections import namedtuple

from dateutil.parser import parse as dateparse

PLPlayerPosition = namedtuple('PlayerPosition', ['name', 'shortname'])

with open('test-files/static-fpl-info.json', 'r') as f:
    data = json.loads(f.read())

POSITION_ID = {
    1: PLPlayerPosition('Goalkeeper', 'GKP'),
    2: PLPlayerPosition('Defender', 'DEF'),
    3: PLPlayerPosition('Midfielder', 'MID'),
    4: PLPlayerPosition('Forward', 'FWD'),
}

class PLTeam:
    def __init__(self, id, name, short_name):
        self.id = id
        self.name = name
        self.shortname = short_name

    @classmethod
    def from_api(cls, id, name, short_name, **kw):
        return cls(id, name, short_name)

    def yet_to_play(self, gameweek):
        matches = data['fixtures'][str(gameweek)]
        match = [match
                 for match in matches
                 if match['team_a'] == self.id
                 or match['team_h'] == self.id][0]
        start_time = dateparse(match['kickoff_time']).replace(tzinfo=None)
        return start_time > datetime.datetime.now()

    def is_playing(self, gameweek):
        matches = data['fixtures'][str(gameweek)]
        match = [match
                 for match in matches
                 if match['team_a'] == self.id
                 or match['team_h'] == self.id][0]
        start_time = dateparse(match['kickoff_time']).replace(tzinfo=None)
        return (start_time < datetime.datetime.now()
                < start_time + datetime.timedelta(hours=1, minutes=50))

    def has_played(self, gameweek):
        matches = data['fixtures'][str(gameweek)]
        match = [match
                 for match in matches
                 if match['team_a'] == self.id
                 or match['team_h'] == self.id][0]
        start_time = dateparse(match['kickoff_time']).replace(tzinfo=None)
        return (datetime.datetime.now()
                > start_time + datetime.timedelta(hours=1, minutes=50))

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
        return PLTEAM_ID[str(self.team_id)]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'{self.__class__.__qualname__}(id={self.pid}, '
                f"name='{self.name}', "
                f'{self.plteam}, '
                f'{self.role})')

PLTEAM_ID = {
   str(i + 1): PLTeam.from_api(**team_data)
               for i, team_data in enumerate(data['teams'])
}

players = {}
for api_player_data in data['elements']:
    player = PLPlayer.from_api(**api_player_data)
    players[player.pid] = player


