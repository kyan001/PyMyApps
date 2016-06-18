import socket, re, ping3, statistics, sys

def getDelays(addr, count, timeout=2):
    delays = []
    none_count = 0
    print('- ping {} ...'.format(addr), end='')
    for i in range(count):
        try:
            delay = ping3.do_one(addr, timeout)
        except Exception as e:
            print()
            print(e)
            input('按回车键继续...')
        if delay:
            delay = delay * 1000
            content = ' {}ms'.format(int(delay))
        else:
            none_count += 1
            content = ' Timeout'
        delays.append(delay)
        sys.stdout.write(content)
        sys.stdout.flush()
        if none_count > 4:
            break
    print()
    return delays

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

def ping_this(addr, title, count=10):
    print(title+'：')
    delays = getDelays(addr, count)
    analyse = analyseDelays(delays)
    for k, v in analyse.items():
        print(v)
    print('\n')

my_ip = socket.gethostbyname(socket.gethostname())
print('本机IP：{}'.format(my_ip))
ip_pattern = re.compile(r'([0-9]+)\.([0-9]+)\.([0-9]+)\.[0-9]+')
gateway_ip = ip_pattern.sub(r'\1.\2.\3.1', my_ip)
print('网关IP：{}'.format(gateway_ip))
print()
baidu_ip = socket.gethostbyname('baidu.com')
github_ip = socket.gethostbyname("github.com")
google_ip = socket.gethostbyname('google.com')

ping_this(gateway_ip, '检查本机与 路由器 之间的连接', count=20)
ping_this(baidu_ip, '检查本机与 baidu.com 之间的连接')
ping_this(github_ip, '检查本机与 github.com 之间的连接')
ping_this(google_ip, '检查本机与 google.com 之间的连接')

input('按回车键继续...')
