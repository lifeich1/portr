from . import index
from . import utils
from . import auth
import time
import urllib.request
import os

import socketio


def alive_request(url, op, secret, verbose=False):
    token = utils.gen_po_token(time.time(), op, index.keys['salt'], secret)
    if url is None:
        print('token:', token)
        return
    resp = urllib.request.urlopen(url + '/' + token)
    ans = resp.read().decode('utf-8')
    if verbose:
        print('token: %r, resp: %r' % (token, ans))
    if ans != 'OK':
        print('error: %r' % ans)


def test_main():
    alive_request('http://localhost:7070/ka', 'a', index.keys['secret'], verbose=True)

def main(url, op, secret):
    alive_request(url, op, secret)

def v2main(url, secret):
    sio = socketio.Client()
    check = auth.sy_op_checker(secret)

    def quit_s(signum, frame):
        sio.disconnect()
        exit(0)

    @sio.event
    def connect():
        print("I'm connected!")

    @sio.event
    def sy_shut(data):
        print('got sy_shut')
        if not ('timestamp' in data and 'sign' in data):
            return
        ts = data['timestamp']
        s = data['sign']
        if not check.check(ts, s, 'sy_shut'):
            return
        print('check sy_shut event pass')
        # TODO check remote shutdown cmd
        #sio.disconnect()
        #os.system('sudo systemctl poweroff')

    @sio.event
    def connect_error():
        print("The connection failed!")

    @sio.event
    def disconnect():
        print("I'm disconnected!")

    sio.connect(url)
    import signal
    signal.signal(signal.SIGTERM, quit_s)
    try:
        sio.wait()
    except KeyboardInterrupt:
        quit_s(None, None)
