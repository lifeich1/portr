from . import index
from . import utils
import time
import urllib.request

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


def test_main():
    alive_request('http://localhost:7070/ka', 'a', index.keys['secret'], verbose=True)

def main(url, op, secret):
    alive_request(url, op, secret)
