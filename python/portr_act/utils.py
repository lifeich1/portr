import hashlib
import zlib
import time

_po_tm_fmt = '%Yy%mm%dd%Hh%Mn%S'

def enhance_salt(salt):
    t = hex(zlib.crc32(salt.encode()))
    z = hashlib.sha224((salt + t + salt[1:]).encode())
    return salt * 4 + z.hexdigest() + salt * 5

def enhance_secret(secret, salt):
    t = hex(zlib.crc32(secret.encode()))
    z = hashlib.sha256((secret[1:] + t + salt[::2] + secret).encode())
    return z.hexdigest()

def timestamp2po(stamp):
    return time.strftime(_po_tm_fmt, time.localtime(stamp))

def po2timestamp(po):
    return time.mktime(time.strptime(po, _po_tm_fmt))

def po_checksum(tm, salt, secret):
    return hashlib.md5((tm + secret + salt).encode()).hexdigest()

def gen_po_token(stamp, salt, secret):
    t = timestamp2po(stamp)
    return po_checksum(t, salt, secret) + t

def parse_po_token(token, salt, secret):
    if len(token) <= 32:
        return None
    check, po = token[:32], token[32:]
    try:
        stamp = po2timestamp(po)
    except Exception as e:
        return None
    t = timestamp2po(stamp)
    if po_checksum(t, salt, secret) != check:
        return None
    else:
        return stamp
