#coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
class Spider:
    headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def search(self,movie):
        param={'keyword':movie.encode('gb2312')}
        url='http://so.loldytt.com/search.asp'
        html=requests.post(url,params=param)
        # html=requests.post("http://so.loldytt.com/search.asp?keyword=%B0%A2%B8%CA")
        bsobj=BeautifulSoup(html.text)
        htmlContent=html.text.encode('ISO-8859-1').decode('gb2312')
        urldic=self.matchUrl(htmlContent)
        for i in urldic:
            if i['name']==movie:
                return i
        return urldic

    def matchMagnet(self,html):
        pattern=re.compile(r'thunder://.*="')
        match=pattern.match(html)
        if match:
            print(match.group())

    def matchUrl(self,html):
        pattern=re.compile(r'http://www\.loldytt\.com/.*/.*/">.+</a>')
        urlPattern=re.compile(r'http://www\.loldytt\.com/.*/.*/')
        match=pattern.findall(html)
        lst=[]
        for i in match:
            tmpstr=i.replace('</a>','')
            url=urlPattern.match(tmpstr).group()
            mvName=tmpstr.replace(url+'">','')
            lst.append({'name':mvName,'url':url})
        return lst

if __name__ == '__main__':
    spider=Spider()
    print(spider.search('美国恐怖故事第二季'))
