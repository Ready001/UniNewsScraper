from flask_restful import Resource
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup


class YaleDaily(Resource):
    def get(self):
        request_url = 'http://yaledailynews.com/feed'
        request = urlopen(urllib.request.Request(request_url, None, {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}))
        soup = BeautifulSoup(request, 'lxml')
        retval = []
        first = True
        for x in soup.find_all('item')[:20]:            
            ret = {}
            ret['title'] = x.title.string
            ret['link'] = x.a['href']
            ret['date'] = x.contents[7].string

            ret['desc'] = x.description.get_text().split("...")[0] + "..."

            list_p = x.find('content:encoded').find_all('p')
            content_list = [s.get_text() for s in list_p]
            ret['content'] = content_list[:-3]
            retval.append(ret)

        return {'data':retval}