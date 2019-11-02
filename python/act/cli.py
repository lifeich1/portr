from . import index
from . import utils
import time
import urllib.request

def alive_request(url, secret, verbose=False):
    token = utils.gen_po_token(time.time(), index.keys['salt'], secret)
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
    alive_request('http://localhost:7070/ka', index.keys['secret'], verbose=True)

def main(url, secret):
    alive_request(url, secret)
