import requests
from bs4 import BeautifulSoup

URL = 'http://ldcn-mechatronics.net/publications/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'accept': '*/*'}


def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all('p', class_='tp_pub_title')[00]
    return item.get_text()


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        raise ConnectionError('status != 200')


if __name__ == '__main__':
    print(parse())
