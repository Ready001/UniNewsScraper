from flask_restful import Resource
import json, urllib.request
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

def scraper(url):
    retval = {}
    for i in range(1, 6):
        try:
            request = urlopen(urllib.request.Request(url + 'page/' + str(i), None, {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}))
        except urllib2.HTTPError:
            break
        soup = BeautifulSoup(request, 'html.parser')
        retlist = []
        for j in range(len(soup.find_all(class_='sno-animate')) - 4):
            x = soup.find_all(class_='sno-animate')[j]
            ret = {}
            ret['title'] = x.h1.a.string
            ret['link'] = x.h1.a['href']
            if (x.p.contents[1].name != u'a'):
                ret['date'] = x.p.contents[0]
                ret['journalist'] = None
            else :
                ret['journalist'] = x.p.contents[1].string
                if (x.p.contents[2].name is None):
                    ret['date'] = x.p.contents[4]
                else:
                    ret['date'] = x.p.contents[3]
            if (len(x.p.next_sibling.contents) == 0):
                ret['partialtext'] = None
            else:
                ret['partialtext'] = x.p.next_sibling.contents[0].string
            retlist.append(ret)
        retval['Page ' + str(i)] = retlist
    return retval


class PurdueExponent(Resource):
    def get(self):
        request_url = 'http://www.purdue.edu/newsroom/rss/StudentNews.xml'
        req = requests.get(request_url)
        soup = BeautifulSoup(req.content, 'xml')
        retval = []
        first = True
        for x in soup.find_all('item')[:20]:            
            ret = {}
            ret['title'] = x.title.string
            link = x.link.get_text()
            ret['link'] = link

            ret['date'] = x.pubDate.string

            # desc_full is a string which sometimes starts with the html code for an image
            desc_full = x.description.string
            if desc_full[0] == '<':
                start = desc_full.find("http")
                end = desc_full.find("jpg\"") + 3
                desc_str = desc_full[desc_full.find(">")+1:]
                img = desc_full[start:end]
                ret['desc'] = desc_str
                ret['img_url'] = img
            else:
                ret['desc'] = desc_full                

            # getting page content from link
            try:
                response = urlopen(link)
                content_soup = BeautifulSoup(response.read(), 'html.parser')
                main_content = content_soup.find("div", {"class": "maincontent"})
                list_p = main_content.find_all('p')
                content_list = [s.get_text() for s in list_p]
                ret['content'] = content_list
            except:
                print("error fetching content")

            retval.append(ret)

        return {'data':retval}


if __name__ == '__main__':
    scraper('http://www.purdueexponent.org/campus/')
