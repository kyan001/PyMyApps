import socket
import os
import sys
import re
import configparser
import subprocess
import cmd
from collections import OrderedDict

import consoleiotools as cit  # oip3 install consoleiotools
import KyanToolKit  # pip3 install KyanToolKit


class G(object):
    # values
    myip = socket.gethostbyname(socket.gethostname())
    ippattern = re.compile(r'([0-9]+)\.([0-9]+)\.([0-9]+)\.[0-9]+')
    addrpattern = re.compile(r'([a-zA-Z0-9]+.)+[com|net|me|org|cn|jp|us]')
    gatewayip = ippattern.sub(r'\1.\2.\3.1', myip)
    extfile = os.path.splitext(__file__)[0] + '.ini'
    extfile = extfile if os.path.isfile(extfile) else 'netqual.ini'
    # structures
    ips = OrderedDict()
    delaydict = {}  # each addr's delays
    # strings
    ext_notice = ""


class IShell(cmd.Cmd):
    def __init__(self):
        super().__init__(self)
        self.prompt = '\nNetqual> '
        self.intro = """
欢迎使用 NetPing，输入 ? 查看所有命令
- Ping: ping, ping 1, p, p 1
- 列表：list, ls
- 查看说明：help
- 退出：exit
"""

    def preloop(self):
        KyanToolKit.KyanToolKit.clearScreen()

    def do_ping(self, args):
        name = list(G.ips)[int(args) - 1] if args else cit.get_choice(list(G.ips))
        ip = G.ips[name]
        affix = "-t" if "win" in sys.platform else ''
        command = "ping {ip} {af}".format(ip=ip, af=affix)
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
    do_p = do_ping

    def help_ping(self):
        cit.echo('用系统命令 ping 某个 ip')
        cit.echo('使用语法: ping [index]', lvl=1)
        cit.echo('如果没有提供 index，会让你从列表中选择')
        cit.echo('index 应为数字，从 1 开始')

    def do_list(self, args):
        """显示 ip 列表"""
        for i, (name, ip) in enumerate(G.ips.items()):
            cit.echo('{i}) {n}: {ip}'.format(i=str(i+1).rjust(2), n=name, ip=ip))
    do_ls = do_list

    def do_exit(self, args):
        """Exit"""
        return True
    do_quit = do_exit  # shortcuts


def main():
    init_dicts()
    shell = IShell()
    shell.cmdloop()


def init_dicts():
    """init ips dict and delaydict"""
    config = configparser.ConfigParser()
    if not os.path.isfile(G.extfile):
        config['路由器'] = {
            'ip': G.gatewayip,
            '# ip': 'Can be IP(8.8.8.8) or Address(google.com)',
            'watch': 'yes',
            '# watch': 'Set "yes" to see it in graphic',
            'hline': '10',
            '# hline': 'Draw a horizontal line with given num in ms',
        }
        config['baidu'] = {'ip': 'baidu.com'}
        config['github'] = {'ip': 'github.com'}
        config.write(open(G.extfile, 'w'))
    config.read(G.extfile)
    for s in config.sections():
        sect = config[s]  # get section
        name = s
        # parse ip
        ip = sect.get('ip')
        if G.addrpattern.match(ip):
            ip = socket.gethostbyname(ip)
        if not ip or not G.ippattern.match(ip):
            G.ext_notice += '格式不正确，无法解析 IP：{}'.format(s)
            continue
        # put data
        G.ips[name] = ip
    for k, v in G.ips.items():
        G.delaydict[v] = []

if __name__ == '__main__':
    try:
        main()
    finally:
        print('Exiting {}'.format(__file__))
