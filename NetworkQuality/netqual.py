import socket
import re
import statistics
import queue
import threading
import time
from collections import defaultdict, OrderedDict
from functools import wraps

import ping3
import KyanToolKit
ktk = KyanToolKit.KyanToolKit()


# values
myip = socket.gethostbyname(socket.gethostname())
ippattern = re.compile(r'([0-9]+)\.([0-9]+)\.([0-9]+)\.[0-9]+')
gatewayip = ippattern.sub(r'\1.\2.\3.1', myip)
baiduip = socket.gethostbyname('baidu.com')
githubip = socket.gethostbyname("github.com")
ips = OrderedDict()
ips['路由器'] = gatewayip
ips['国内（baidu.com）'] = baiduip
ips['国外（github.com）'] = githubip
ips['墙外（twitter.com）'] = '37.61.54.158'

# structures
outputq = queue.Queue()  # output queue
delaydict = {}  # each addr's delays
for k, v in ips.items():
    delaydict[v] = []


def main():
    for k in ips:
        start_ping(ips[k])
    while True:
        ktk.clearScreen()
        assemble_print()
        printQ()
        time.sleep(1)


def putPrint(words: str):
    if words:
        outputq.put(words)


def printQ():
    while not outputq.empty():
        print(outputq.get())


def analyseDelays(delays):
    total_count = len(delays)
    none_count = delays.count(None)
    valid_delays = [d for d in delays if d]
    result = {}
    if none_count == total_count:
        result['error'] = '- 连接失败：{} 次尝试均无响应'.format(total_count)
    else:
        if total_count:
            none_rate = int(none_count / total_count * 100)
            result['connectivity'] = '- 【无响应率】{}%：\t'.format(none_rate)
            if none_rate > 50:
                result['connectivity'] += '[差] 连通性差，上网体验差'
            elif none_rate > 10:
                result['connectivity'] += '[中] 连通性中等，但可能会影响游戏体验'
            elif none_rate > 0:
                result['connectivity'] += '[良] 连通性良好，较顺畅'
            else:
                result['connectivity'] += '[优] 连通性优秀，无 timeout'

        if len(valid_delays) > 1:
            mean = int(statistics.mean(valid_delays))
            result['latency'] = '- 【平均延迟】{}ms：\t'.format(mean)
            if mean > 1000:
                result['latency'] += '[差] 平均延迟异常，网络响应过慢'
            elif mean > 200:
                result['latency'] += '[中] 平均延迟偏高，可能会影响游戏体验'
            elif mean > 100:
                result['latency'] += '[良] 平均延迟良好'
            else:
                result['latency'] += '[优] 平均延迟优秀，可愉快的玩耍'

            variance = int(statistics.variance(valid_delays))
            result['stability'] = '- 【延迟方差】{}：\t'.format(variance)
            if variance > 10000:
                result['stability'] += '[差] 连接稳定性差，响应速度忽快忽慢'
            elif variance > 2500:
                result['stability'] += '[中] 连接稳定性中等，可能会影响游戏体验'
            elif variance > 100:
                result['stability'] += '[良] 连接稳定性良好，游戏上网两不误'
            else:
                result['stability'] += '[优] 连接稳定性优秀，击败了全国 99% 的电脑'
    return result


def assemble_session(dest, addr):
    putPrint('本机 <--> {}：'.format(dest))

    pingstr = '- ping {}：'.format(addr)
    delaylist = delaydict[addr]
    for d in delaylist:
        pingstr += '{}ms'.format(d) if d is not None else 'Timeout'
        pingstr += '\t'
    putPrint(pingstr)

    analyse = analyseDelays(delaylist)
    for k, v in analyse.items():
        putPrint(v)
    putPrint(' ')


def assemble_print():
    putPrint('网络质量监控：')
    putPrint('=' * 25)
    putPrint(' ')
    putPrint('本机 IP：{}'.format(myip))
    putPrint('网关 IP：{}'.format(gatewayip))
    putPrint(' ')
    for k, v in ips.items():
        assemble_session(k, v)


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
        try:
            delay = ping3.do_one(addr, timeout)
        except Exception as e:
            print(e)
            input('按回车键继续...')
        if delay:
            if delay < 0.5:
                time.sleep(0.5 - delay)
            delay = int(delay * 1000)
        delaydict[addr].append(delay)
        if not running:
            break


if __name__ == '__main__':
    try:
        running = True
        main()
    except KeyboardInterrupt:
        running = False
