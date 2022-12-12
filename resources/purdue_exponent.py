from flask_restful import Resource
import requests
from bs4 import BeautifulSoup

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
