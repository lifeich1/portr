import configparser
import os

config  = configparser.ConfigParser()

secret = 'testtest'
fn = '/var/opt/portr-act.ini'

if os.path.exists(fn):
    config.read(fn)
    if 'srv' in config and 'secret' in config['srv']:
        secret = config['srv']['secret']

import portr_act

portr_act.index.update_params(secret=secret)
application = portr_act.index.app.wsgifunc()
