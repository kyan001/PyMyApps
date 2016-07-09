import socket
import os
import re
import statistics
import queue
import threading
import time
from collections import OrderedDict
from functools import wraps

import ping3
import KyanToolKit
ktk = KyanToolKit.KyanToolKit()


class G(object):
    # values
    myip = socket.gethostbyname(socket.gethostname())
    ippattern = re.compile(r'([0-9]+)\.([0-9]+)\.([0-9]+)\.[0-9]+')
    addrpattern = re.compile(r'([a-zA-Z0-9]+.)+[com|net|me|org|cn|jp|us]')
    gatewayip = ippattern.sub(r'\1.\2.\3.1', myip)
    baiduip = socket.gethostbyname('baidu.com')
    githubip = socket.gethostbyname("github.com")
    extfile = os.path.splitext(__file__)[0] + '.txt'
    # structures
    outputq = queue.Queue()  # output queue
    ips = OrderedDict()
    delaydict = {}  # each addr's delays
    # strings
    ext_notice = ""
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


def init_dicts(ips, delay):
    """init ips dict and delaydict"""
    ips['路由器'] = G.gatewayip
    ips['国内（baidu.com）'] = G.baiduip
    ips['国外（github.com）'] = G.githubip
    if os.path.isfile(G.extfile):
        with open(G.extfile, 'r') as f:
            for l in f:
                l = l.strip()
                if l[0] == '#' or not l:  # comments or empty
                    continue
                ext_item = l.split()
                if len(ext_item) == 1 and G.addrpattern.match(ext_item[0]):
                    G.ips[ext_item[0]] = socket.gethostbyname(ext_item[0])
                elif len(ext_item) != 2:  # not a valid
                    G.ext_notice += '格式不正确: {}\n'.format(l)
                elif not G.ippattern.match(ext_item[1]):  # not a ip
                    G.ext_notice += '不是有效 IP: {}\n'.format(l)
                else:
                    G.ips[ext_item[0]] = ext_item[1]
    else:
        G.ext_notice += '\n- 未找到外部配置文件：' + G.extfile
        G.ext_notice += """
- 外部文件请按照每行 “名称 ip” 的格式，或以网址单独一行，注释以“#”开头。
- 例：
    # 游戏类
    Wakfu 52.76.139.242

    # 网站类
    superfarmer.net
        """
    for k, v in ips.items():
        delay[v] = []


def main():
    init_dicts(G.ips, G.delaydict)
    try:
        ping3.do_one(G.myip, 1)  # test ping
    except OSError as e:
        ktk.err(e)
        ktk.info('可能您需要以管理员权限运行')
        ktk.pressToContinue()
        ktk.bye()
    for k in G.ips:
        start_ping(G.ips[k])
    while True:
        ktk.clearScreen()
        assemble_print()
        printQ()
        time.sleep(0.6)


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
            result['connectivity'] = '无响应率 {}%：'.format(none_rate)
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
            result['latency'] = '平均延迟 {}ms：'.format(mean)
            if mean > 1000:
                result['latency'] += '差'
            elif mean > 200:
                result['latency'] += '中'
            elif mean > 100:
                result['latency'] += '良'
            else:
                result['latency'] += '优'

            variance = int(statistics.variance(valid_delays))
            result['stability'] = '延迟方差 {}：'.format(variance)
            if variance > 10000:
                result['stability'] += '差'
            elif variance > 2500:
                result['stability'] += '中'
            elif variance > 100:
                result['stability'] += '良'
            else:
                result['stability'] += '优'
    for i in result:
        result[i] = '【' + result[i] + '】'
    return result


def assemble_session(dest, addr):
    putPrint('*')
    putPrint('| {}：ping {}'.format(dest, addr))
    # analyse
    delaylist = G.delaydict[addr][-50:]  # only calc last 50
    analyse = analyseDelays(delaylist)
    summery = '| '
    for k, v in analyse.items():
        summery += v + '\t'
    putPrint(summery)
    # pings
    pingstr = '| '
    for d in delaylist[-10:]:
        pingstr += '\t{}ms'.format(d) if d is not None else '\tTimeout'
    putPrint(pingstr)
    putPrint('|')


def assemble_print():
    putPrint('网络质量监控：')
    putPrint('=' * 25)
    putPrint('本机 IP：{}'.format(G.myip))
    putPrint('网关 IP：{}'.format(G.gatewayip))
    putPrint(' ')
    putPrint(G.quality_expl.strip())
    putPrint(' ')
    for k, v in G.ips.items():
        assemble_session(k, v)
    putPrint('=' * 25)
    putPrint(G.ext_notice)


def async(input_func: callable):  # decorator
    """使函数单开一个线程执行"""
    @wraps(input_func)
    def callInputFunc(*args, **kwargs):
        t = threading.Thread(target=input_func, args=args, kwargs=kwargs)
        t.start()
        return t
    return callInputFunc


@async
def start_ping(addr, timeout=3):
    while True:
        delay = ping3.do_one(addr, timeout)
        if delay:
            if delay < 1:
                time.sleep(1 - delay)
            delay = int(delay * 1000)
        G.delaydict[addr].append(delay)
        if not running:
            break


if __name__ == '__main__':
    try:
        running = True
        main()
    finally:
        print('Exiting {}'.format(__file__))
        running = False
