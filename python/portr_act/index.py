import web
import time
import hashlib
import os
import shelve

from . import utils

urls = (
    '/', 'hello',
    '/q', 'query',
    '/q/(.*)', 'query',
    '/ka/(.*)', 'keepalive'
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

_zero_cache_dict = {
    'first_active_time': 0.0,
    'last_active_time': 0.0,
    'active_op': 'b'
}

_order_cache_keys = (
    'first_active_time',
    'last_active_time',
    'active_op',
)

def _cadic2tup(d):
    return tuple([d[k] for k in _order_cache_keys])

def get_last():
    p = keys['lastdate_cache']
    try:
        with shelve.open(p) as db:
            for k in _order_cache_keys:
                if k not in db:
                    return _zero_cache_dict
            return dict(**db)
    except ValueError as e:
        print('corrupted cache file')
    return _zero_cache_dict

def store_last(l, first_a=None, op=None):
    u = dict(last_active_time=l, active_op=('a' if op is None else op))
    if first_a is not None:
        u['first_active_time'] = first_a
    p = keys['lastdate_cache']
    with shelve.open(p, writeback=True) as db:
        db.update(u)

def is_alive_info(l, op):
    return (time.time() - l < keys['dead_dur']) and (op == 'a')

def is_alive():
    d = get_last()
    _, l, op = _cadic2tup(d)
    return is_alive_info(l, op), d

class hello:
    def GET(self):
        global keys
        al, info = is_alive()
        fr, la, _ = _cadic2tup(info)
        ret = 'Hello + ' + '\nstartup: ' + time.ctime(keys['startup'])\
            + '\nalive: ' + str(al) + '\nnow: ' + time.ctime()
        if la > 0:
            ret += '\nlast register: ' + time.ctime(la)\
                + '\nthis reboot begin: ' + time.ctime(fr)
        return ret

class query:
    def GET(self, op=None):
        if op == 'first':
            fr = get_last()['first_active_time']
            return int(fr)
        else:
            return 'ALIVE' if is_alive()[0] else 'DEAD'

class keepalive:
    def GET(self, token):
        global keys
        stamp, op = utils.parse_po_token(token, keys['salt'], keys['secret'])
        if stamp is None:
            return 'Invalid'
        else:
            _, l, lop = _cadic2tup(get_last())
            if l < stamp:
                d = {}
                if not is_alive_info(l, lop):
                    d = dict(first_a=stamp)
                store_last(stamp, op=op, **d)
            return 'OK'

import socketio

def test_main(w=False):
    if w:
        mgr = socketio.KombuManager('amqp://', write_only=True)
        mgr.emit('sy_shutdown', {'sign':'abcd','timestamp':time.time()},room='defa')
        return
    mgr = socketio.KombuManager('amqp://')
    sio = socketio.Server(client_manager=mgr, async_mode='threading')

    @sio.event
    def connect(sid, environ):
        print('+++ online', sid)
        sio.enter_room(sid, 'defa')
        sio.emit('sy_shutdown', {'sign':'abcd','timestamp':time.time()},room='defa')

    @sio.event
    def disconnect(sid):
        print('+++ offline', sid)

    from flask import Flask
    app = Flask(__name__)
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    app.run(threaded=True)





#def test_main():
#    import sys
#    if len(sys.argv) > 1:
#        sys.argv[1] = '7070'
#    app.run()

def update_params(**kwargs):
    global keys
    if 'secret' in kwargs:
        kwargs['secret'] = utils.enhance_secret(kwargs['secret'], keys['salt'])
    keys.update(kwargs)
