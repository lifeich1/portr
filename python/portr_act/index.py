import web
import time
import hashlib
import os

from . import utils
from .model import KAModel
import socketio

urls = (
    '/', 'hello',
    '/q', 'query',
    '/q/(.*)', 'query',
    '/ka/(.*)', 'keepalive',
    '/da/(.*)', 'remote_shut',
)
app = web.application(urls, globals())

keys = dict(
    startup=time.time(),
    dead_dur=240,
    lastdate_cache='/var/tmp/portr-alive_cache',
    salt='107180ee55419c' + '5eab1b0cbd56d1' + '7324923f071b48'
    + '50c2d0df75bab' + '1afee0da61f0e5',
    secret='testtest'
)
keys['salt'] = utils.enhance_salt(keys['salt'])

_mod = None

def _touch_mod():
    global _mod
    if _mod is None:
        _mod = KAModel(keys['lastdate_cache'])

def get_last():
    _touch_mod()
    global _mod
    _mod.sync()
    return _mod.data

_store_last_core = None

def store_last(l, first_a=None, op=None):
    _touch_mod()
    global _store_last_core
    if _store_last_core is None:
        global _mod
        @_mod.commit
        def ss(l, first_a, op):
            global _mod
            t = _mod.data
            if first_a is not None:
                t = t._replace(first_active_time=first_a)
            if op is None:
                op = 'a'
            t = t._replace(last_active_time=l, active_op=op)
            _mod.data = t
        _store_last_core = ss
    return _store_last_core(l, first_a, op)


class hello:
    def GET(self):
        global keys, _mod
        _touch_mod()
        _mod.sync()
        al, info = _mod.is_alive(keys['dead_dur']), _mod.data
        fr, la = info.first_active_time, info.last_active_time
        ret = 'Hello + ' + '\nstartup: ' + time.ctime(keys['startup'])\
            + '\nalive: ' + str(al) + '\nnow: ' + time.ctime()
        if la > 0:
            ret += '\nlast register: ' + time.ctime(la)\
                + '\nthis reboot begin: ' + time.ctime(fr)
        return ret

class query:
    def GET(self, op=None):
        if op == 'first':
            fr = get_last().first_active_time
            return int(fr)
        else:
            _touch_mod()
            global _mod
            _mod.sync()
            return 'ALIVE' if _mod.is_alive(keys['dead_dur']) else 'DEAD'

class keepalive:
    def GET(self, token):
        global keys
        stamp, op = utils.parse_po_token(token, keys['salt'], keys['secret'])
        if stamp is None:
            return 'Invalid'
        else:
            info = get_last()
            l, lop = info.last_active_time, info.active_op
            if l < stamp:
                d = {}
                global _mod
                if not _mod.is_alive(keys['dead_dur']):
                    d = dict(first_a=stamp)
                store_last(stamp, op=op, **d)
            return 'OK'

import socketio

class remote_shut:
    def GET(self, token):
        mgr = socketio.KombuManager('amqp://', write_only=True)
        mgr.emit('sy_shut', data={'foo':'bar'}, room='pi')
        return 'send shutdown'


#def test_main(w=False):
#    if w:
#        mgr = socketio.KombuManager('amqp://', write_only=True)
#        mgr.emit('sy_shutdown', {'sign':'abcd','timestamp':time.time()},room='defa')
#        return
#    mgr = socketio.KombuManager('amqp://')
#    sio = socketio.Server(client_manager=mgr, async_mode='threading')
#
#    @sio.event
#    def connect(sid, environ):
#        print('+++ online', sid)
#        sio.enter_room(sid, 'defa')
#        sio.emit('sy_shutdown', {'sign':'abcd','timestamp':time.time()},room='defa')
#
#    @sio.event
#    def disconnect(sid):
#        print('+++ offline', sid)
#
#    from flask import Flask
#    app = Flask(__name__)
#    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
#    app.run(threaded=True)





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
