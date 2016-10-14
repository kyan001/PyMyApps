import socket
import os
import sys
import re
import statistics
import queue
import threading
import time
import configparser
import subprocess
import cmd
from collections import OrderedDict
from functools import wraps

import ping3
import consoleiotools as cit
import KyanToolKit  # pip3 install KyanToolKit
ktk = KyanToolKit.KyanToolKit()


class G(object):
    # values
    myip = socket.gethostbyname(socket.gethostname())
    ippattern = re.compile(r'([0-9]+)\.([0-9]+)\.([0-9]+)\.[0-9]+')
    addrpattern = re.compile(r'([a-zA-Z0-9]+.)+[com|net|me|org|cn|jp|us]')
    gatewayip = ippattern.sub(r'\1.\2.\3.1', myip)
    extfile = os.path.splitext(__file__)[0] + '.ini'
    # structures
    outputq = queue.Queue()  # output queue
    ips = OrderedDict()
    delaydict = {}  # each addr's delays
    # strings
    ext_notice = ""
    running = False


class IShell(cmd.Cmd):
    def __init__(self):
        super().__init__(self)
        self.prompt = '\nNetqual> '
        self.intro = """
欢迎使用 NetQual，输入 ? 查看所有命令
- 启动/停止/查看：start、stop、state
- 文字展示: show 1、show
- Ping: ping 1
- 查看说明：expl
- 退出：exit
"""

    def preloop(self):
        time.sleep(2)
        ktk.clearScreen()

    def do_state(self, args):
        """显示程序的运行状态"""
        cit.info('Running: {}'.format('On' if G.running else 'Off'))

    def do_show(self, args):
        """显示所有 ping 的细节信息

        语法：ping [count]
        count - 一共刷新多少次，不填则无限循环
        """
        count = int(args) if args.isdigit() else 0
        while (not args) or count > 0:
            time.sleep(0.6)
            ktk.clearScreen()
            assemble_print()
            printQ()
            count -= 1

    def do_start(self, args):
        """开始运行 ping（需配合 show）"""
        if not G.running:
            G.running = True
            for k in G.ips:  # starting ping those IPs
                ktk.info('启动 {}'.format(k))
                start_ping(G.ips[k])
        else:
            ktk.warn('已在运行中')

    def do_stop(self, args):
        """停止运行 ping"""
        G.running = False
        ktk.info('已停止运行')

    def do_ping(self, args):
        name = list(G.ips)[int(args) - 1] if args else ktk.getChoice(list(G.ips))
        ip = G.ips[name]
        affix = "-t" if "win" in sys.platform else ''
        command = "ping {ip} {af}".format(ip=ip, af=affix)
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def help_ping(self):
        ktk.echo('用系统命令 ping 某个 ip')
        ktk.echo('使用语法: ping [index]', lvl=1)
        ktk.echo('如果没有提供 index，会让你从列表中选择')
        ktk.echo('index 应为数字，从 1 开始')

    def do_expl(self, args):
        """显示对延迟、方差、稳定性的解释"""
        quality_expl = """
- 【无响应率】：
    [优] 连通性优秀，无 timeout
    [良] 连通性良好，较顺畅
    [中] 连通性中等，但可能会影响游戏体验
    [差] 连通性差，上网体验差
- 【平均延迟】：
    [优] 平均延迟优秀，可愉快的玩耍
    [良] 平均延迟良好
    [中] 平均延迟偏高，可能会影响游戏体验
    [差] 平均延迟异常，网络响应过慢
- 【延迟方差】：
    [优] 连接稳定性优秀，击败了全国 99% 的电脑
    [良] 连接稳定性良好，游戏上网两不误
    [中] 连接稳定性中等，可能会影响游戏体验
    [差] 连接稳定性差，响应速度忽快忽慢
        """
        for line in quality_expl.strip().split('\n'):
            ktk.info(line)

    def do_exit(self, args):
        """Exit interactive shell mode & stop running"""
        G.running = False
        return True
    do_quit = do_exit  # shortcuts


def async(input_func: callable):  # decorator
    """使函数单开一个线程执行"""
    @wraps(input_func)
    def callInputFunc(*args, **kwargs):
        t = threading.Thread(target=input_func, args=args, kwargs=kwargs)
        t.start()
        return t
    return callInputFunc


def main():
    init_dicts()
    try:
        ping3.do_one(G.myip, 1)  # test ping
    except OSError as e:
        ktk.err(e)
        ktk.info('可能您需要以管理员权限运行')
        ktk.pressToContinue()
        ktk.bye()
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
        config['国内（baidu）'] = {'ip': 'baidu.com'}
        config['国外（github）'] = {'ip': 'github.com'}
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


def putPrint(words: str):
    if words:
        G.outputq.put(words)


def printQ():
    while not G.outputq.empty():
        print(G.outputq.get())


def analyseDelays(delays):
    total_count = len(delays)
    none_count = delays.count(None)
    valid_delays = [d for d in delays if d]
    result = {}
    if none_count == total_count:
        result['error'] = '连接失败：{} 次尝试均无响应'.format(total_count)
    else:
        if total_count:
            none_rate = int(none_count / total_count * 100)
            result['connectivity'] = 'disc {}% '.format(none_rate)
            if none_rate > 50:
                result['connectivity'] += '差'
            elif none_rate > 10:
                result['connectivity'] += '中'
            elif none_rate > 0:
                result['connectivity'] += '良'
            else:
                result['connectivity'] += '优'

        if len(valid_delays) > 1:
            mean = int(statistics.mean(valid_delays))
            result['latency'] = 'late {}ms '.format(mean)
            if mean > 1000:
                result['latency'] += '差'
            elif mean > 200:
                result['latency'] += '中'
            elif mean > 100:
                result['latency'] += '良'
            else:
                result['latency'] += '优'

            variance = int(statistics.variance(valid_delays))
            result['stability'] = 'stab {} '.format(variance)
            if variance > 10000:
                result['stability'] += '差'
            elif variance > 2500:
                result['stability'] += '中'
            elif variance > 100:
                result['stability'] += '良'
            else:
                result['stability'] += '优'
    return result


def assemble_session(dest, addr):
    putPrint('*')
    # analyse
    delaylist = G.delaydict[addr][-50:]  # only calc last 50
    analyse = analyseDelays(delaylist)
    summery = ''
    for k, v in analyse.items():
        summery += '\t[' + v + ']'
    # pings
    pingstr = '| '
    for d in delaylist[-10:]:
        pingstr += '\t{}ms'.format(d) if d is not None else '\t--'
    putPrint('| {} {}: {}'.format(dest, addr, summery))
    putPrint(pingstr)
    putPrint('|')


def assemble_print():
    putPrint('本机 IP：{}'.format(G.myip))
    putPrint('网关 IP：{}'.format(G.gatewayip))
    putPrint(' ')
    putPrint('运行状态：{}'.format('运行中' if G.running else '已停止'))
    for k, v in G.ips.items():
        assemble_session(k, v)
    putPrint('=' * 25)
    putPrint(G.ext_notice)


@async
def start_ping(addr, timeout=3):
    while G.running:
        delay = ping3.do_one(addr, timeout)
        if delay:
            if delay < 1:
                time.sleep(1 - delay)
            delay = int(delay * 1000)
        G.delaydict[addr].append(delay)


if __name__ == '__main__':
    try:
        main()
    finally:
        G.running = False
        print('Exiting {}'.format(__file__))
