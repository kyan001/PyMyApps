import os
import sys
import json

import consoleiotools as cit


# Set environment variables through python script does not work. Run it in your shell manually.
__version__ = "1.0.0"


CONFIG_FILE = "config.json"
CONFIG_KEYS = ("address", "username", "password")
CONFIGS = {}


def __run_cmd(cmd: str) -> bool:
    """run command and return if its result"""
    SUCCESS_CODE = 0
    cit.echo(cmd, "Command")
    return os.system(cmd) == SUCCESS_CODE


def get_proxy_commands(address: str = CONFIGS.get('address')) -> dict:
    """Get proxy setting commands for different platforms"""
    if sys.platform.startswith('win'):
        return {
            'start': [
                'set http_proxy={}'.format(address),
                'set https_proxy={}'.format(address),
            ],
            'stop': [
                'set http_proxy=',
                'set https_proxy=',
            ],
        }
    else:  # Linux and macOS
        return {
            'start': [
                'export http_proxy={}'.format(address),
                'export https_proxy={}'.format(address),
            ],
            'stop': [
                'unset http_proxy',
                'unset https_proxy',
            ],
        }


def add_proxy_auth_info(username: str = CONFIGS.get('username'), password: str = CONFIGS.get('password'), address: str = CONFIGS.get('address')):
    """Add username and password info, return proxy string with auth info added"""
    if sys.platform.startswith('win'):
        return __run_cmd("set http_proxy_user={}".format(username)) and __run_cmd("set http_proxy_pass={}".format(password))
    else:
        protocol, server = address.split('://')
        return "{protocol}://{username}:{password}@{server}".format(protocol=protocol, username=username, password=password, server=server)


@cit.as_session
def start_proxy(address: str = CONFIGS.get('address')):
    commands = get_proxy_commands(address)
    for command in commands.get('start'):
        if not __run_cmd(command):
            return False
    return True


@cit.as_session
def stop_proxy() -> bool:
    commands = get_proxy_commands()
    for command in commands.get('stop'):
        if not __run_cmd(command):
            return False
    return True


@cit.as_session("Proxy Status")
def show_proxy_status():
    http_proxy = os.environ.get("http_proxy")
    https_proxy = os.environ.get("https_proxy")
    if http_proxy:
        cit.info("HTTP Proxy = {}".http_proxy)
    else:
        cit.info("No HTTP Proxy Set.")
    if https_proxy:
        cit.info("HTTPS Proxy = {}".https_proxy)
    else:
        cit.info("No HTTPS Proxy Set.")


@cit.as_session("Config Status")
def show_config_status():
    for key in CONFIG_KEYS:
        cit.info("{key} = {val}".format(key=key, val=CONFIGS.get(key)))


def status():
    show_proxy_status()
    show_config_status()


@cit.as_session
def load_config_file():
    """Load config file into CONFIGS"""
    if CONFIG_FILE and os.path.isfile(CONFIG_FILE):
        configs = json.load(CONFIG_FILE)
        for key in CONFIG_KEYS:
            val = configs.get(key)
            if val:
                CONFIGS[key] = val
                cit.info("Config set: {key} = {val}".format(key=key, val=val))
            else:
                cit.info("Config ignored: {key}")
    else:
        cit.warn("Config file does not exist")


if __name__ == '__main__':
    import shellproxy_cli
    shellproxy_cli.main()
