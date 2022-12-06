from flask_restful import Resource
import json, urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup

base_url = 'http://dailyillini.com/category/'

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


class News(Resource):
    def get(self, category):
        request_url = base_url + category + '/'
        return scraper(request_url)

class SubCategoryNews(Resource):
    def get(self, category, subcategory):
        request_url = base_url + category + '/' + subcategory + '/'
        return scraper(request_url)

class SportsNews(Resource):
    def get(self, category, subcategory, sportcategory):
        request_url = base_url + category + '/' + subcategory + '/' + sportcategory + '/'
        return scraper(request_url)

class RecentNews(Resource):
    def get(self):
        request_url = 'http://dailyillini.com/feed/'
        request = urlopen(urllib.request.Request(request_url, None, {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}))
        soup = BeautifulSoup(request, 'lxml')
        retval = []
        first = True
        for x in soup.find_all('item'):            
            ret = {}
            ret['title'] = x.title.string
            ret['link'] = x.a['href']
            ret['date'] = x.contents[7].string

            ret['desc'] = x.description.get_text().split("...")[0] + "..."

            img = x.description.a.find('img')
            if img != None:
                try:
                    srcset = img['srcset']
                    srcset = srcset.split(", ")
                    nums = []
                    links = []
                    maxVal = 0
                    maxIndex = 0
                    for index,src in enumerate(srcset):
                        splitSrc = src.split(' ')
                        links.append(splitSrc[0])
                        num = int(splitSrc[1][:-1])
                        nums.append(num)
                        if num > maxVal:
                            maxVal = num
                            maxIndex = index
                    ret['img_url'] = links[maxIndex]
                except:
                    print("failed to get image")

            list_p = x.find('content:encoded').find_all('p')
            content_list = [s.get_text() for s in list_p]
            ret['content'] = content_list[:-3]
            retval.append(ret)

        return {'data':retval}


if __name__ == '__main__':
    scraper('http://dailyillini.com/category/news/champaign-urbana/')
