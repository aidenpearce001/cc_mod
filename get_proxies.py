import requests
import json
from bs4 import BeautifulSoup
import re 
import threading
import time
import sys

SSL = 'https://www.sslproxies.org/'
FREE_PROXY = 'https://free-proxy-list.net/'
SPYS_ME = "https://spys.one/en/socks-proxy-list/"
PROXYSCRAPE = 'https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=us&ssl=all&anonymity=all'
PROXYNOVA = 'https://www.proxynova.com/proxy-server-list/'
PROXYLIST_DOWNLOAD_HTTP = 'https://www.proxy-list.download/HTTP'
PROXYLIST_DOWNLOAD_HTTPS = 'https://www.proxy-list.download/HTTPS'
PROXYLIST_DOWNLOAD_SOCKS4 = 'https://www.proxy-list.download/SOCKS4'
PROXYLIST_DOWNLOAD_SOCKS5 = 'https://www.proxy-list.download/SOCKS5'
proxy_cz = "http://free-proxy.cz/en/proxylist/country/all/socks5/ping/all/2"
hidemy_socks5 = "https://hidemy.name/en/proxy-list/?type=5&start={}"
hidemy_socks4 = "https://hidemy.name/en/proxy-list/?type=4&start={}"
proxy_scan = "https://www.proxyscan.io/download?type={}"

mapping_port = {}
nums = 0

def downloadsocks(mode):
	if mode == "socks4":
		f = open("socks.txt",'wb')
		try:
			r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",timeout=5)
			f.write(r.content)
		except:
			pass
		try:
			r = requests.get("https://www.proxy-list.download/api/v1/get?type=socks4",timeout=5)
			f.write(r.content)
		except:
			pass
		try:
			r = requests.get("https://www.proxyscan.io/download?type=socks4",timeout=5)
			f.write(r.content)
		except:
			pass
		try:
			r = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",timeout=5)
			f.write(r.content)
			f.close()
		except:
			f.close()
            
		try:
			r = requests.get("https://www.socks-proxy.net/",timeout=5)
			part = str(r.content)
			part = part.split("<tbody>")
			part = part[1].split("</tbody>")
			part = part[0].split("<tr><td>")
			proxies = ""
			for proxy in part:
				proxy = proxy.split("</td><td>")
				try:
					proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
				except:
					pass
				out_file = open("socks4.txt","a")
				out_file.write(proxies)
				out_file.close()
		except:
			pass

	if mode == "socks5":
		f = open("socks.txt",'wb')
		try:
			r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true",timeout=5)
			f.write(r.content)
		except:
			pass
		try:
			r = requests.get("https://www.proxy-list.download/api/v1/get?type=socks5",timeout=5)
			f.write(r.content)
		except:
			pass
		try:
			r = requests.get("https://www.proxyscan.io/download?type=socks5",timeout=5)
			f.write(r.content)
		except:
			pass
		try:
			r = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",timeout=5)
			f.write(r.content)
		except:
			pass
		try:
			r = requests.get("https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",timeout=5)
			f.write(r.content)
			f.close()
		except:
			f.close()

def proxy_archive():

    from datetime import datetime

    archive_api = f"https://checkerproxy.net/api/archive/{datetime.today().strftime('%Y-%m-%d')}"
    proxy_archive = requests.get(archive_api).json()

    proxy_list = [i['addr'] if i['timeout'] < 3001 else None for i in proxy_archive]
    proxy_list = [i for i in proxy_list if i]

    return proxy_list

def port_porcess(port_char):

    port = ""
    
    for i in port_char.split("+"):
        char = re.sub(r'[^\w]', ' ',i).split(" ")

        port = port + str(mapping_port[char[1]] ^ mapping_port[char[2]])
        
    return port

def SPYS_ME_SOCKS():
    
    socks_list = []

    headers = {
      'Connection': 'keep-alive',
      'Pragma': 'no-cache',
      'Cache-Control': 'no-cache',
      'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
      'sec-ch-ua-mobile': '?0',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
      'Origin': 'https://spys.one',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-User': '?1',
      'Sec-Fetch-Dest': 'document',
      'Referer': 'https://spys.one/en/socks-proxy-list/',
      'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7'
    }

    preprocess = requests.request("POST", SPYS_ME, headers=headers)
    presoup = BeautifulSoup(preprocess.text,"html.parser")
    payload = "xx0="+presoup.find(attrs={"name" : "xx0"})['value'] + "&xpp=5&xf1=0&xf2=0&xf4=0&xf5=2"
    print(payload)
    
    spys = requests.request("POST", SPYS_ME, headers=headers, data=payload)
    soup = BeautifulSoup(spys.text,"html.parser")
    
    method = re.findall('<script type="text/javascript">(.*);</script>',str(soup.find('script', type="text/javascript")))[0].split(";")

    for i in method[:10]:
        mapping_port[i.split("=")[0]] = int(i.split("=")[1])

    for i in method[10:]:
        ops = i.split("=")[1].split("^")
        mapping_port[i.split("=")[0]] = int(ops[0]) ^ mapping_port[ops[1]]

    for tr in soup.findAll("tr",{"class":"spy1xx"}):
        ip = tr.find('font').text
        raw_js = tr.find('script')
        port_char = re.findall(r'font class=spy2>:<\\/font>"\+(.*)\)</script>',str(raw_js))[0]

        socks_list.append(ip+":"+port_porcess(port_char))

    for tr in soup.findAll("tr",{"class":"spy1x"}):
        try:
            ip = tr.find('font').text
            raw_js = tr.find('script')
            port_char = re.findall(r'font class=spy2>:<\\/font>"\+(.*)\)</script>',str(raw_js))[0]

            socks_list.append(ip+":"+port_porcess(port_char))
        except:
            continue

    return socks_list

def hidemy_socks(mode):
    start = 0
    socks_list = []
    
    hidemy_headers = {
      'authority': 'hidemy.name',
      'pragma': 'no-cache',
      'cache-control': 'no-cache',
      'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
      'sec-ch-ua-mobile': '?0',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-user': '?1',
      'sec-fetch-dest': 'document',
      'referer': 'https://hidemy.name/en/proxy-list/?type=5&start=64',
      'accept-language': 'vi,en-US;q=0.9,en;q=0.8,vi-VN;q=0.7'
    }

    print(mode)
    if mode == 'socks5':
        hidemy_url = hidemy_socks5.format(start)
    elif mode == 'socks4':
        hidemy_url = hidemy_socks4.format(start)
      
    print(hidemy_url)
    res = requests.get(hidemy_url,headers=hidemy_headers)
    soup = BeautifulSoup(res.content,"html.parser")
    hidemy_pages = soup.find('div',{'class':'pagination'}).findAll('a')
        
    for page in range(len(hidemy_pages)-1):
        res = requests.get(hidemy_url,headers=hidemy_headers)
        soup = BeautifulSoup(res.content,"html.parser")
        if soup.find('tbody').text == ' ':
            break
        else:
            socks = soup.find('tbody').findAll('tr')
            for sock in socks:
                
                socks_list.append(sock.findAll('td')[0].text+":"+sock.findAll('td')[1].text)
    
        start +=64

    return socks_list 

def proxyscan_socks(mode):

    socks_list = []

    if mode == 'socks5':
        mod = 5
    elif mode == 'socks4':
        mod = 4

    r = requests.get(proxy_scan.format(mode), allow_redirects=True)
    open(mode+'.txt', 'wb').write(r.content)
    
    with open(mode+'.txt','r+') as f:
        for _ in f:
            socks_list.append(_.rstrip())

    return socks_list	
def get_all(socks_type):

    proxies = set()
    downloadsocks(socks_type)

    socks_list = open('socks.txt').readlines()
    for i in socks_list:
        proxies.add(i)
    for i in hidemy_socks(socks_type):
        proxies.add(i)
    for i in proxyscan_socks(socks_type):
        proxies.add(i)
        
    return proxies

def checking(lines,socks_type,ms,rlock,):
    global nums
    proxy = lines.strip().split(":")
    if len(proxy) != 2:
        rlock.acquire()
        socks_list.remove(lines)
        rlock.release()
        return
    err = 0
    while True:
        if err >= 3:
            rlock.acquire()
            socks_list.remove(lines)
            rlock.release()
            break
        try:
            s = socks.socksocket()
            if socks_type == 4:
                s.set_proxy(socks.SOCKS4, str(proxy[0]), int(proxy[1]))
            if socks_type == 5:
                s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s.settimeout(ms)
            s.connect((str(target), int(port)))
            if protocol == "https":
                ctx = ssl.SSLContext()
                s = ctx.wrap_socket(s,server_hostname=target)
            sent = s.send(str.encode("GET / HTTP/1.1\r\n\r\n"))
            if not sent:
                err += 1
            s.close()
            break
        except:
            err +=1
    nums += 1

def check_socks(ms, socks_type):
    global nums
    global socks_list

    thread_list=[]
    rlock = threading.RLock()

    socks_list = list(get_all(socks_type=socks_type))
    for lines in socks_list:
        print(lines)
        if socks_type == "socks5":
            th = threading.Thread(target=checking,args=(lines,5,ms,rlock,))
            th.start()
        if socks_type == "socks4":
            th = threading.Thread(target=checking,args=(lines,4,ms,rlock,))
            th.start()
        thread_list.append(th)
        time.sleep(0.01)
        sys.stdout.write("> Checked "+str(nums)+" proxies\r")
        sys.stdout.flush()
    for th in list(thread_list):
        th.join()
        sys.stdout.write("> Checked "+str(nums)+" proxies\r")
        sys.stdout.flush()
    print("\r\n> Checked all proxies, Total Worked:"+str(len(socks_list)))
    ans = input("> Do u want to save them in a file? (y/n, default=y)")

    if socks_type == "socks4":
        with open("socks.txt", 'wb') as fp:
            for lines in list(proxies):
                fp.write(bytes(lines,encoding='utf8'))
        fp.close()
    elif socks_type == "socks5":
        with open("socks.txt", 'wb') as fp:
            for lines in list(proxies):
                fp.write(bytes(lines,encoding='utf8'))

# check_socks(ms, socks_type =5)
# SPYS_ME_SOCKS()
# print(SPYS_ME_SOCKS())
check_socks(5,socks_type='socks5')
