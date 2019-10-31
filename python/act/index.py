import web
import time
import hashlib

from . import utils

urls = (
    '/', 'hello',
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

class hello:
    def GET(self):
        return 'Hello + ' + '\nstartup: ' + time.ctime(keys['startup'])\
            + '\nalive: ' + str(time.time() - keys['last'] < keys['dead_dur'])

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
