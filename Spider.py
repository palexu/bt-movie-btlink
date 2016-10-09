#coding=utf-8
from bs4 import BeautifulSoup
import requests
import urllib.parse
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

        movieCount=self.__getNumOfMovie(htmlContent)
        print('为你找到了%d部电影～回复序号获得迅雷链接'%movieCount)
        urllist=[]
        n=movieCount//20
        m=movieCount%20
        if m>0:
            n=n+1
        for i in range(1,n+1):
            param={'keyword':Transfer.toGb2312(movie),'page':i}
            html=requests.post(url,params=param)
            bsobj=BeautifulSoup(html.text, "html.parser")
            htmlContent=Transfer.toUtf8(html.text)
            urllist.append(self.__matchUrl(htmlContent))
        rs=[]
        for i in urllist:
            for j in i:
                rs.append(j)
        return rs

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
        urlPattern=re.compile(r'http://www\.loldytt\.com/[\w|\d]+/[\w|\d]+/')
        match=pattern.findall(html)

        lst=[]
        for i in match:
            tmpstr=i.replace('</a>','')
            url=urlPattern.match(tmpstr).group()
            mvName=tmpstr.replace(url+'">','')
            lst.append({'name':mvName,'url':url})
        return lst

    def __getNumOfMovie(self,html):
        pattern=re.compile(r'共找到<b>\d+</b>部')
        match=pattern.findall(html)
        if match:
            num=match[0].replace('共找到<b>','').replace('</b>部','')
            return int(num)

    def found(self,movie,inputList):
        for i in inputList:
            if movie==i['name']:
                return i['url']
        return False


class Movie:
    
    def getMovie(self,movie):
        spider=Spider()
        rs=spider.search(movie)
        hasFound=spider.found(movie,rs)
        # if hasFound:
        #     result=spider.getMagnet(hasFound)
        #     for item in result:
        #         print("%s  %s"%(item['name'],item['thunderLink']))
        # else:
        #     for i in rs:
        #         print(i['name'])
        for index,item in enumerate(rs):
            print('%d.%s'%(index,item['name']))


class test:
    def printMovieInfo(self):
        print("""美国恐怖故事第二季EP01  thunder://QUFmdHA6Ly90djp0dkB4bGguMnR1LmNjOjMxNDU2L8PAufq/1rLAucrKwrXatv68vi9b0bjA18/C1Nh3d3cuMnR1LmNjXcPAufq/1rLAucrKwi612rb+vL5FUDAxLnJtdmJaWg==\n
美国恐怖故事第二季EP02  thunder://QUFmdHA6Ly9kczpkc0B4bGMuMnR1LmNjOjIxMjkyL8PAufq/1rLAucrKwrXatv68vi9b0bjA18/C1Nh3d3cuMnR1LmNjXcPAufq/1rLAucrKwi612rb+vL5FUDAyLnJtdmJaWg==\n
美国恐怖故事第二季EP03  thunder://QUFmdHA6Ly9kczpkc0B4bGMuMnR1LmNjOjIxMjk2L8PAufq/1rLAucrKwrXatv68vi9b0bjA18/C1Nh3d3cuMnR1LmNjXcPAufq/1rLAucrKwi612rb+vL5FUDAzLnJtdmJaWg==\n
美国恐怖故事第二季EP04  thunder://QUFmdHA6Ly9kczpkc0B4bGMuMnR1LmNjOjMxMjE3L8PAufq/1rLAucrKwrXatv68vi9b0bjA18/C1Nh3d3cuMnR1LmNjXcPAufq/1rLAucrKwi612rb+vL5FUDA0LnJtdmJaWg==\n
""")

    def test_matchMagnet(self):
        sp=Spider()
        tt='<a href="thunder://QUFmdHA6Ly9keTpkeUB4bGEueHVuYm8uY2M6MTAzNjgvW9G4wNfPwtTYd3d3Llh1bkJvLkNjXbCiuMrV/bSrQkQxMDI0uN/H5dbQ06LLq9fWLnJtdmJaWg==" title="阿甘正传BD1024高清中英双字" target="_self">阿甘正传BD1024高清中英双字</a>'
        print(spider.matchMagnet(tt))

    def test_isUrlCode(self):
        testString='E6%B5%8B%E你8%AF%95'
        print(isUrlCode(testString))


class Transfer:
    def toGb2312(text):
        return text.encode('gb2312')

    def toUtf8(text):
        return text.encode('ISO-8859-1').decode('gb2312')

def isUrlCode(code):
    #有问题
    match=re.match(r'^[%\w]+$',code)
    if match:
        return True
    else:
        return False

if __name__ == '__main__':
    if len(sys.argv)>=2:
        movie=sys.argv[1]
        if movie=='test':
            te=test()
            te.printMovieInfo()
            # te.test_isUrlCode()
        else:
            movie=urllib.parse.unquote(movie)
            movieHandler=Movie()
            movieHandler.getMovie(movie)

    
