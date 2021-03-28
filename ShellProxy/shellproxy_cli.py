import argparse

import shellproxy


def main(assigned_args: list = None):
    parser = argparse.ArgumentParser(prog="shellproxy", description="Set proxy on command-line.", epilog="")
    parser.add_argument("-v", "--version", action="version", version=shellproxy.__version__)
    parser.add_argument(dest="command", metavar="COMMAND", nargs="?", default="status", help="The command for shellproxy: `start`, `stop` or `status`.")
    parser.add_argument("-a", "--address", dest="address", metavar="ADDRESS", default="http://127.0.0.1:1080", help="The address of you proxy. Default is 'https://127.0.0.1:1080'")
    parser.add_argument("-u", "--username", dest="username", metavar="USERNAME", default="", help="The username of your proxy. Default is ''.")
    parser.add_argument("-p", "--password", dest="password", metavar="PASSWORD", default="", help="The password of your proxy. Default is ''.")
    args = parser.parse_args(assigned_args)
    if args.address:
        shellproxy.CONFIGS['address'] = args.address
    if args.username or args.password:
        shellproxy.CONFIGS['username'] = args.username
        shellproxy.CONFIGS['password'] = args.password
    if args.command == 'start':
        shellproxy.start_proxy()
    elif args.command == 'stop':
        shellproxy.stop_proxy()
    elif args.command == 'status':
        shellproxy.status()
    else:
        raise Exception("Command not support: {}".format(args.command))


if __name__ == "__main__":
    main()
