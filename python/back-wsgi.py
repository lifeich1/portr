from gevent import monkey
monkey.patch_all()

import configparser
import socketio
import os

config  = configparser.ConfigParser()

kw = dict(async_mode='gevent_uwsgi')
fn = '/var/opt/portr-act.ini'

if os.path.exists(fn):
    config.read(fn)
    if 'back' in config:
        d = dict(config['back'])
        if 'async_mode' in d:
            del d['async_mode']
        kw.update(d)

import portr_act

sio = portr_act.back.create_server(**kw)
app = socketio.WSGIApp(sio)
