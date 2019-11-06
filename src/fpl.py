import datetime
import json
import time
from collections import namedtuple

from . import static
from . import api
from .utils import star2map, TimedCache

league_data = api.StaticInfo.noslack_league()
static_info = api.StaticInfo.premier_league()

GAMEWEEK = static_info['events']['current']
GameweekInfo = namedtuple('GameweekInfo', ['managers', 'gameweek'])

class Manager:
    def __init__(self, team_id, name, team_name, points=0):
        self.team_id = team_id
        self.name = name
        self.team_name = team_name
        self.points = points

        # Ugly style, but it will do for now
        self.team = None
        self.gw_points = 0

    @classmethod
    def from_api(cls, entry_id, short_name, entry_name,
                 total, event_total, **kw):
        """Create a manager from API data

        Creates a Manager object from API data.
        A Manager is an FPL manager in the NOSLACK FPL league.

        This constructor is created to be called using dictionary destructuring, e.g:
        ```python
        >>> data_from_fpl = fetch_data_from_fpl()
        >>> manager = Manager.from_api(**data_from_fpl)
        ```

        Arguments:
            entry_id {int} -- The id of the manager
            short_name {str} -- The initials of the manager, i.e 'JM' for Jonas Moll
            entry_name {str} -- The full name of the manager, i.e 'Jonas Moll'
            total {int} -- The current total of points the manager has
            event_total {int} -- The number of points gathered the current game week
            **kw {dict} -- Remaining, unused parameters. These are tossed

        Returns:
            [type] -- [description]
        """
        return cls(entry_id, short_name, entry_name, total - event_total)

    def fetch_gw_team(self, gw):
        info = api.DynamicInfo.team_gameweek_stats(self.team_id, gw)
        return Team(info['picks'])

class Team:
    def __init__(self, players):
        self.players = list(star2map(Player.from_api, players))

    def players_on_field(self):
        return list(player for player in self.players
                           if player.position < 12)

    def get_players_at_position(self, position, on_field=True):
        return [player
                for player in self.players
                if player.static.role.shortname.lower() == position.lower()
                and player.on_field is on_field]

    def current_points(self, data):
        return [player.points_from_data(data)
                for player in self.players_on_field()]

class Player:
    def __init__(self, player_id, position):
        self.id = player_id
        self.position = position
        self.static = static.players[self.id]
        self.events = []

    @classmethod
    def from_api(cls, element, position, *args, **kw):
        return cls(element, position)

    @property
    def gw_points(self):
        return sum(event.points for event in self.events)

    @property
    def on_field(self):
        return self.position < 12

    @property
    def benched(self):
        return self.position >= 12

    def will_be_benched(self, gameweek):
        return (self.static.plteam.has_played(gameweek)
                and self.events[0].points == 0)

    def point_events_from_data(self, data):
        events =  list(star2map(PlayerEvent.from_api,
                                data['elements'][str(self.id)]['explain'][0][0]))
        self.events = events
        return events

    def points_from_data(self, data):
        return data['elements'][str(self.id)]['stats']['total_points']

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'{self.__class__.__qualname__}(id={self.id}, '
                f'position={self.position}, {self.static})')

class PlayerEvent:
    def __init__(self, event, points, count, event_name):
        self.event = event
        self.points = points
        self.count = count
        self.event_name = event_name

    @classmethod
    def from_api(cls, name, points, value, stat, **kw):
        return cls(stat, points, value, name)

    @property
    def unit_point(self):
        return round(self.points / self.count, 2) if self.count > 0 else 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f"{self.__class__.__qualname__}(event='{self.event}', "
                f'points={self.points}, count={self.count}, '
                f"event_name='{self.event_name}', unit_point={self.unit_point}")

# Setup static team information
team_data = [
    {**team_info, **standings_info}
    for standings_info in league_data['standings']
    for team_info in league_data['league_entries']
    if standings_info['league_entry'] == team_info['id']
]

@TimedCache(datetime.timedelta(minutes=1))
def get_current_state():
    managers = list(star2map(Manager.from_api, team_data))
    gameweek = api.StaticInfo.premier_league()['events']['current']
    teams = [manager.fetch_gw_team(gameweek)
             for manager in managers]

    current_info = api.DynamicInfo.gameweek_stats(gameweek)

    gw_points = [sum(team.current_points(current_info))
                 if team is not None else 0
                 for team in teams]

    for manager, team, points in zip(managers, teams, gw_points):
        manager.team = team
        manager.gw_points = points
        for player in manager.team.players:
            player.point_events_from_data(current_info)

    managers = sorted(managers, key=lambda m: m.points + m.gw_points,
                      reverse=True)

    return GameweekInfo(managers, gameweek)

