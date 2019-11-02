import web
import time
import hashlib

from . import utils

urls = (
    '/', 'hello',
    '/q', 'query',
    '/ka/(.*)', 'keepalive'
)
app = web.application(urls, globals())

keys = dict(
    startup=time.time(),
    last=0,
    dead_dur=120,
    salt='107180ee55419c' + '5eab1b0cbd56d1' + '7324923f071b48'
    + '50c2d0df75bab' + '1afee0da61f0e5',
    secret='testtest'
)
keys['salt'] = utils.enhance_salt(keys['salt'])

def is_alive():
    return time.time() - keys['last'] < keys['dead_dur']

class hello:
    def GET(self):
        al = is_alive()
        ret = 'Hello + ' + '\nstartup: ' + time.ctime(keys['startup'])\
            + '\nalive: ' + str(al) + '\nnow: ' + time.ctime()
        if keys['last'] > 0:
            ret += '\nlast register: ' + time.ctime(keys['last'])
        return ret

class query:
    def GET(self):
        return 'ALIVE' if is_alive() else 'DEAD'

class keepalive:
    def GET(self, token):
        stamp = utils.parse_po_token(token, keys['salt'], keys['secret'])
        if stamp is None:
            return 'Invalid'
        else:
            keys['last'] = max(stamp, keys['last'])
            return 'OK'

def test_main():
    import sys
    if len(sys.argv) > 1:
        sys.argv[1] = '7070'
    app.run()
