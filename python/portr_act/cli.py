from . import index
from . import utils
import time
import urllib.request

import socketio

def test_main():
    sio = socketio.Client()

    def quit_s(signum, frame):
        sio.disconnect()
        exit(0)

    @sio.event
    def sy_shutdown(data):
        print('recv data:', data)

    sio.connect("http://localhost:5000")
    import signal
    signal.signal(signal.SIGTERM, quit_s)
    try:
        sio.wait()
    except KeyboardInterrupt:
        quit_s(None, None)



def alive_request(url, op, secret, verbose=False):
    token = utils.gen_po_token(time.time(), op, index.keys['salt'], secret)
    if url is None:
        print('token:', token)
        return
    # TODO send token
    resp = urllib.request.urlopen(url + '/' + token)
    ans = resp.read().decode('utf-8')
    if verbose:
        print('token: %r, resp: %r' % (token, ans))
    if ans != 'OK':
        print('error: %r' % ans)


#def test_main():
#    alive_request('http://localhost:7070/ka', 'a', index.keys['secret'], verbose=True)

#def main(url, op, secret):
#    alive_request(url, op, secret)
