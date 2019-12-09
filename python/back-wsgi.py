import configparser
import socketio
import os

config  = configparser.ConfigParser()

kw = dict(async_mode='gevent_uwsgi')
fn = '/var/opt/portr-act.ini'

if os.path.exists(fn):
    config.read(fn)
    if 'back' in config and 'kombu-url' in config['back']:
        kw['kombu_url'] = config['back']['kombu-url']

import portr_act

sio = portr_act.back.create_server(**kw)
application = socketio.WSGIApp(sio)
