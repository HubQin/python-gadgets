import requests
from bs4 import BeautifulSoup

def get_response(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
        'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWYzN2U1MzE0OTc4MTEyZmUzYjYxODM2NjA0NjQxNmZmBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWpKWkM5MUxkdVhxTUtvWDlBdmlJZG9xRG1mY3dqSUlyNjhKSzMreXd4S2M9BjsARg%3D%3D--ab59ddc1eaf683ceb355a49c90b031ca8c4b0ec1; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1540393845,1540473107,1540512299,1540553043; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1540553309'
    }
    response = requests.get(url, headers = headers)
    return response

def parse_one_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', id='ip_list')
    trs = table.find_all('tr')
    trs = trs[1:]
    for tr in trs:
        tds = tr.find_all('td')
        if 'HTTPS' in tds[5].text and 'fast' in str(tds[6]):
            ip = tds[1].text
            port = tds[2].text
            # is_ok = check_ip(ip,port)
            # if is_ok:
            yield ip, port

# def check_ip(ip, port):
#     proxies = {}
#     headers = {
#         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
#     }
#     ip = 'http://' + ip + ':' + port
#     proxies['http'] = ip
#     test_url = 'https://www.baidu.com/'
#     try:
#         response = requests.get( , headers = headers, proxies = proxies)
#         if response.status_code == 200:
#             print(response.status_code)
#             print('AAA\n')
#             return True
#         else:
#             print('A001\n')
#             return False
#     except:
#         return False

def save_ip(ip, port):
    with open('ip_list.txt', 'a') as f:
        f.write(ip + ':' + port + '\n')
        f.close()

if __name__ == '__main__':
    url_format = 'http://www.xicidaili.com/nn/{}'
    for page in range(1,100):
        url = url_format.format(page)
        response = get_response(url)
        data = parse_one_page(response)
        for x in data:
            save_ip(x[0],x[1])
            print(x[0] + ' success!')