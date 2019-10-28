import datetime
from functools import wraps

star2map = lambda func, seq: map(lambda obj: func(**obj), seq)

class TimedCache:
    def __init__(self, time=datetime.timedelta(minutes=1)):
        self.cache_duration = time
        self.cached_time = datetime.datetime.now()
        self.cached_result = None

    def _should_cache_update(self):
        return (self.cached_result is None
                or (datetime.datetime.now() - self.cached_time) > self.cache_duration)

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kw):
            if self._should_cache_update():
                print('Updating...')
                self.cached_result = func(*args, **kw)
            return self.cached_result
        return inner
