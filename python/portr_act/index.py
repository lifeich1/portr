import web
import time
import hashlib
import os

from . import utils

urls = (
    '/', 'hello',
    '/q', 'query',
    '/ka/(.*)', 'keepalive'
)
app = web.application(urls, globals())

keys = dict(
    startup=time.time(),
    dead_dur=240,
    lastdate_cache='/var/tmp/portr-alive.cache',
    salt='107180ee55419c' + '5eab1b0cbd56d1' + '7324923f071b48'
    + '50c2d0df75bab' + '1afee0da61f0e5',
    secret='testtest'
)
keys['salt'] = utils.enhance_salt(keys['salt'])

def get_last():
    p = keys['lastdate_cache']
    if os.path.exists(p):
        try:
            with open(p, 'r') as f:
                s = f.readline().split()
                t = s[0]
                op = s[1] if len(s) > 1 else 'a'
                return float(t), op
        except ValueError as e:
            print('corrupted cache file')
    return 0.0, 'b'

def store_last(l, op=None):
    if op is None:
        op = 'a'
    p = keys['lastdate_cache']
    with open(p, 'w') as f:
        print(l, op, file=f)

def is_alive():
    l, op = get_last()
    return (time.time() - l < keys['dead_dur']) and (op == 'a'), l

class hello:
    def GET(self):
        global keys
        al, la = is_alive()
        ret = 'Hello + ' + '\nstartup: ' + time.ctime(keys['startup'])\
            + '\nalive: ' + str(al) + '\nnow: ' + time.ctime()
        if la > 0:
            ret += '\nlast register: ' + time.ctime(la)
        return ret

class query:
    def GET(self):
        return 'ALIVE' if is_alive()[0] else 'DEAD'

class keepalive:
    def GET(self, token):
        global keys
        stamp, op = utils.parse_po_token(token, keys['salt'], keys['secret'])
        if stamp is None:
            return 'Invalid'
        else:
            l, _ = get_last()
            if l < stamp:
                store_last(stamp, op)
            return 'OK'

def test_main():
    import sys
    if len(sys.argv) > 1:
        sys.argv[1] = '7070'
    app.run()

def update_params(**kwargs):
    global keys
    if 'secret' in kwargs:
        kwargs['secret'] = utils.enhance_secret(kwargs['secret'], keys['salt'])
    keys.update(kwargs)
