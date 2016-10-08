#coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import sys


class Spider:
    headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def search(self,movie):
        param={'keyword':Transfer.toGb2312(movie)}
        url='http://so.loldytt.com/search.asp'
        html=requests.post(url,params=param)
        bsobj=BeautifulSoup(html.text, "html.parser")
        htmlContent=Transfer.toUtf8(html.text)
        urldic=self.__matchUrl(htmlContent)
        return urldic

    def __matchMagnet(self,text):
        pattern=re.compile(r'thunder:\/\/[A-Za-z0-9\+\/=]*')
        match=pattern.findall(text)
        if match:
            return match[0]
        else:
            return ''

    def getMagnet(self,url):
        html=requests.get(url)
        bsobj=BeautifulSoup(Transfer.toUtf8(html.text), "html.parser")
        lst=[]
        for i in bsobj.find_all('a',{'target':'_self'}):
            rs=self.__matchMagnet(str(i))
            if rs!='':
                lst.append({'name':i.get_text(),'thunderLink':rs})
        return lst

    def __matchUrl(self,html):
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

    def found(self,movie,inputList):
        for i in inputList:
            if movie==i['name']:
                return i['url']
        return False


class Movie:
    spider=Spider()

    def getMovie(self,movie):
        rs=spider.search(movie)
        hasFound=spider.found(movie,rs)
        if hasFound:
            result=spider.getMagnet(hasFound)
            for item in result:
                print("%s  %s"%(item['name'],item['thunderLink']))
        else:
            for i in rs:
                print(i['name'])


class test:
    def printMovieInfo(self):
        print("""美国恐怖故事第二季EP01  thunder://QUFmdHA6Ly90djp0dkB4bGguMnR1LmNjOjMxNDU2L8PAufq/1rLAucrKwrXatv68vi9b0bjA18/C1Nh3d3cuMnR1LmNjXcPAufq/1rLAucrKwi612rb+vL5FUDAxLnJtdmJaWg==
美国恐怖故事第二季EP02  thunder://QUFmdHA6Ly9kczpkc0B4bGMuMnR1LmNjOjIxMjkyL8PAufq/1rLAucrKwrXatv68vi9b0bjA18/C1Nh3d3cuMnR1LmNjXcPAufq/1rLAucrKwi612rb+vL5FUDAyLnJtdmJaWg==
美国恐怖故事第二季EP03  thunder://QUFmdHA6Ly9kczpkc0B4bGMuMnR1LmNjOjIxMjk2L8PAufq/1rLAucrKwrXatv68vi9b0bjA18/C1Nh3d3cuMnR1LmNjXcPAufq/1rLAucrKwi612rb+vL5FUDAzLnJtdmJaWg==
美国恐怖故事第二季EP04  thunder://QUFmdHA6Ly9kczpkc0B4bGMuMnR1LmNjOjMxMjE3L8PAufq/1rLAucrKwrXatv68vi9b0bjA18/C1Nh3d3cuMnR1LmNjXcPAufq/1rLAucrKwi612rb+vL5FUDA0LnJtdmJaWg==
""")

    def test_matchMagnet(self,text):
        sp=Spider()
        tt='<a href="thunder://QUFmdHA6Ly9keTpkeUB4bGEueHVuYm8uY2M6MTAzNjgvW9G4wNfPwtTYd3d3Llh1bkJvLkNjXbCiuMrV/bSrQkQxMDI0uN/H5dbQ06LLq9fWLnJtdmJaWg==" title="阿甘正传BD1024高清中英双字" target="_self">阿甘正传BD1024高清中英双字</a>'
        print(spider.matchMagnet(tt))


class Transfer:
    def toGb2312(text):
        return text.encode('gb2312')

    def toUtf8(text):
        return text.encode('ISO-8859-1').decode('gb2312')


if __name__ == '__main__':
    if len(sys.argv)>=2:
        movie=sys.argv[1]
        if movie=='test':
            te=test()
            te.printMovieInfo()
        else:
            movieHandler=Movie()
            movieHandler.getMovie(movie)

    
