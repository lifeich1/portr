import hashlib
import base64
import time


class sy_op_checker:
    def __init__(self, secret):
        t = hashlib.sha512(secret.encode()).hexdigest()
        self._secret = t.lower()
        self._ts = int(time.time())

    def sign(self, timestamp, data=None):
        t = str(timestamp) + self._secret
        if data is not None:
            t = t + str(data)
        z = hashlib.sha256(t.encode()).digest()
        s = base64.b32encode(z).decode()
        return s

    def check(self, timestamp, sign, data=None):
        timestamp = int(timestamp)
        if self._ts >= timestamp:
            return False
        s = self.sign(timestamp, data)
        print(repr(s), repr(sign))
        return s == sign
