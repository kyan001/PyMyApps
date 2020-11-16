import urllib.request
import consoleiotools as cit


def check_proxy_and_site(url: str, proxy: str = None) -> bool:
    cit.info(f"checking {url} @ {proxy}")

    if proxy:
        proxy_handler = urllib.request.ProxyHandler({
            "http": proxy,
            "https": proxy,
        })
        url_opener = urllib.request.build_opener(proxy_handler)
    else:
        url_opener = urllib.request.build_opener()
    url_opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(url_opener)
    try:
        sock = urllib.request.urlopen(url, timeout=15)
    except urllib.error.URLError as err:
        cit.warn(err)
        return False
    except Exception as err:
        cit.warn(err)
        return False
    cit.info("Success")
    return True


def check(url: str, proxy: str):
    BAIDU = "https://www.baidu.com"
    GOOGLE = "https://www.google.com"
    if not url.startswith("http"):
        url = "http://" + url
    if not check_proxy_and_site(url=BAIDU):
        cit.err("Current network is NOT OK.")
        cit.bye()
    if check_proxy_and_site(url=GOOGLE):
        cit.warn("Current Network already out of GFW.")
    if not check_proxy_and_site(proxy=proxy, url=GOOGLE):
        cit.err("Proxy `{}` is NOT OK.".format(proxy))
        cit.bye()
    can_visit_inside = check_proxy_and_site(url=url)
    can_visit_outside = check_proxy_and_site(proxy=proxy, url=url)
    if not can_visit_inside and can_visit_outside:
        cit.warn(f"URL `{url}` is BLOCKED BY GFW.")
    if can_visit_inside and not can_visit_outside:
        cit.warn(f"URL `{url}` is MAINLAND ONLY.")
    if not can_visit_inside and not can_visit_outside:
        cit.err(f"URL `{url}` is UNAVAILABLE.")
    if can_visit_inside and can_visit_outside:
        cit.info(f"URL `{url}` is FREE TO VISIT.")
