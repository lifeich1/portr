import shelve
import collections

_fields = (
    'first_active_time',
    'last_active_time',
    'active_op',
)

_defv_fields = (0.0, 0.0, 'b')

def dic2list(d):
    return [d[k] for k in _fields]

def check_parse_db(db, dtype):
    for k in _fields:
        if k not in db:
            return dtype._make(_defv_fields)
    return dtype._make(dic2list(db))

class KAModel:
    def __init__(self, path):
        self._path = path
        data_t = collections.namedtuple('data_t', _fields)
        self._data_t = data_t
        self.keepalive = False
        self.sync()

    def sync(self):
        try:
            with shelve.open(self._path) as db:
                self.data = check_parse_db(db, self._data_t)
                return self.data
        except ValueError as e:
            print('corrupted cache file')
        self.data = self._data_t._make(_defv_fields)
        return self.data

    def commit(self, func):
        def f(*args, **kwargs):
            with shelve.open(self._path, writeback=True) as db:
                self.data = check_parse_db(db, self._data_t)
                ret = func(*args, **kwargs)
                db.update(self.data._asdict())
                return ret
        return f

    def is_alive(self, dead_dur):
        l = self.data.last_active_time
        op = self.data.active_op
        return ((time.time() - l < dead_dur) or self.keepalive) and (op == 'a')
