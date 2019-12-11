import argparse

parser = argparse.ArgumentParser(description='keep alive page')
parser.add_argument('--test', action='store_true', help='test mode')
parser.add_argument('-s', '--secret', default='testtest', help='token secret')

subparsers = parser.add_subparsers(dest='command')

p_srv = subparsers.add_parser('srv')
p_srv.add_argument('-w', action='store_true')

p_cli = subparsers.add_parser('cli')

p_cli.add_argument('-u', '--url', default='http://localhost:7070/ka', help='keepalive target url prefix')
p_cli.add_argument('-c', '--cookie', default='cookie', help='connect cookie')

p_back = subparsers.add_parser('back')
p_back.add_argument('-w', action='store_true')

args = parser.parse_args()

def test_main():
    if args.command == 'srv':
        from . import index
        index.test_main()
    elif args.command == 'cli':
        from . import cli
        cli.test_main(args.secret)
    elif args.command == 'back':
        from . import back
        back.test_main(args.w, secret=args.secret)
    else:
        raise NotImplementedError

if args.test:
    test_main()
    exit()

from . import index
from . import utils
secret = utils.enhance_secret(args.secret, index.keys['salt'])

if args.command == 'cli':
    from . import cli
    cli.v2main(args.url, args.secret, args.cookie)
else:
    raise NotImplementedError
