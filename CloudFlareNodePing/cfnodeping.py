import ipaddress
import threading
import random
import urllib.request
import os

import ping3
import consoleiotools as cit
import consolecmdtools as cct


# CloudFlare Offical IPs can be found here: https://www.cloudflare.com/ips/
# Text IPs: https://www.cloudflare.com/ips-v4
ips_file = os.path.join(cct.get_dir(__file__), "ips.txt")
is_update = cit.get_input("Update IP list from CloudFlare? (y/[n])")
if is_update and is_update.lower() == 'y':
    request = urllib.request.Request("https://www.cloudflare.com/ips-v4", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'})
    cct.update_file(ips_file, request)
with open(ips_file) as fl:
    CLOUDFLARE_IP_NETWORKS = fl.read().split()
# CLOUDFLARE_IP_NETWORKS = ["173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22", "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20", "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/12", "172.64.0.0/13", "131.0.72.0/22"]


def pping_ipa(ip: str, mutex):
    if not isinstance(ip, str):
        ip = str(ip)
    delay = ping3.ping(ip, timeout=4, unit='ms')
    if delay:
        with mutex:
            cit.info(f"{ip}: {int(delay)}ms")


def pping_ipn(ip_network: str):
    mutex = threading.Lock()
    ipn = ipaddress.ip_network(ip_network)
    for ip in ipn:
        threading.Thread(target=pping_ipa, args=(ip, mutex)).start()


def main():
    mutex = threading.Lock()
    for cloudflare_ip_network in CLOUDFLARE_IP_NETWORKS:
        ipn = ipaddress.ip_network(cloudflare_ip_network)
        threading.Thread(target=pping_ipa, args=(random.choice([ip for ip in ipn.hosts()]), mutex)).start()
    with mutex:
        cit.ask("Select a IP Network to ping:")
        ip_network = cit.get_choice(CLOUDFLARE_IP_NETWORKS, exitable=True)
    if ip_network:
        pping_ipn(ip_network)


if __name__ == '__main__':
    main()
