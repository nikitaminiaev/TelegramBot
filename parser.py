import requests
from bs4 import BeautifulSoup


class Parser:
    URL_MECHATRONICS = 'http://ldcn-mechatronics.net/publications/'
    URL_GOOGLE_BLOG = 'https://ai.googleblog.com/'
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'accept': '*/*'}

    def __get_html(self, url, params=None):
        return requests.get(url, headers=Parser.HEADERS, params=params)

    def __get_content(self, html: str, tag='', html_class=''):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find_all(tag, class_=html_class)[00]

    def parse_mechatronics(self):
        html = self.__get_html(Parser.URL_MECHATRONICS)
        if html.status_code == 200:
            item = self.__get_content(html.text, 'p', 'tp_pub_title')

            return item.get_text()
        else:
            raise ConnectionError('status != 200')

    def parse_google_blog(self):
        html = self.__get_html(Parser.URL_GOOGLE_BLOG)
        if html.status_code == 200:
            item = self.__get_content(html.text, 'h2', 'title')

            return item.get_text().replace('\n', '')
        else:
            raise ConnectionError('status != 200')


if __name__ == '__main__':
    parser = Parser()
    print(parser.parse_mechatronics())
    print(parser.parse_google_blog())
