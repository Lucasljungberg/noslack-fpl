import requests as r

BASE_URL = "https://draft.premierleague.com/api/"

class RequestSession(r.Session):
    def __init__(self, base=BASE_URL, *args, **kw):
        super().__init__(*args, **kw)
        self.base = base

    @staticmethod
    def url_join(*parts):
        return '/'.join(part.strip().strip('/') for part in parts)

    def request(self, method, url, **kw):
        modified_url = self.url_join(self.base, url)
        return super().request(method, modified_url, **kw)

session = RequestSession()
LEAGUE_ID = "305"
LEAGUE_INFO = f'/league/{LEAGUE_ID}/details'
STATIC_TEAM_INFO = '/entry/{id}/public'
TEAM_GW_INFO_URL = '/entry/{id}/event/{gw}'
GAMEWEEK_STATS = '/event/{gw}/live'
STATIC_INFO = '/bootstrap-static'

class StaticInfo:
    @staticmethod
    def noslack_league():
        return session.get(LEAGUE_INFO).json()

    @staticmethod
    def premier_league():
        return session.get(STATIC_INFO).json()

class DynamicInfo:
    @staticmethod
    def gameweek_stats(gw):
        return session.get(GAMEWEEK_STATS.format(gw=gw)).json()
    
    @staticmethod
    def team_gameweek_stats(team_id, gw):
        return session.get(TEAM_GW_INFO_URL.format(id=team_id,
                                                   gw=gw)).json()
