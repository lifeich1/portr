from . import index
from . import utils
import time

def alive_request(url, secret):
    token = utils.gen_po_token(time.time(), index.keys['salt'], secret)
    if url is None:
        print('token:', token)
        return
    # TODO send token


def test_main():
    alive_request(None, index.keys['secret'])
