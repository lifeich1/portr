import argparse

parser = argparse.ArgumentParser(description='keep alive page')
parser.add_argument('--test', action='store_true', help='test mode')

subparsers = parser.add_subparsers(dest='command')

p_srv = subparsers.add_parser('srv')
p_cli = subparsers.add_parser('cli')

args = parser.parse_args()

def test_main():
    if args.command == 'srv':
        from . import index
        index.test_main()
    elif args.command == 'cli':
        from . import cli
        cli.test_main()
    else:
        raise NotImplementedError

if args.test:
    test_main()
    exit()

raise NotImplementedError
