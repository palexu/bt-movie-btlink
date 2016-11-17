#coding=utf-8
"""
usage:
python spider.py mv 西瓜

source: ~/code/python/scrap/Movie
"""
from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
import sys
from selenium import webdriver
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
    filename='spider.log',
    filemode='a'
    )

def click():
    driver = webdriver.PhantomJS(executable_path="/Users/xj/program/phantomjs-2.1.1-macosx/bin/phantomjs")
    driver.get("http://so.loldytt.com/search.asp")
    driver.find_element_by_xpath("/html/body/center/div[2]/div[2]/form/input[2]").click()
    driver.close()


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
        # print(htmlContent)
        movieCount=self.__getNumOfMovie(htmlContent)
        if movieCount==None:
            print("获取电影失败，可能是目标网站无响应")
            logging.error("获取电影失败，可能是目标网站无响应")
            return []
        print('为你找到了%d部电影～回复序号获得迅雷链接'%movieCount)
        
        n=movieCount//20
        m=movieCount%20
        if m>0:
            n=n+1

        urllist=[]
        for i in range(1,n+1):
            param={'keyword':Transfer.toGb2312(movie),'page':i}
            html=requests.post(url,params=param)
            bsobj=BeautifulSoup(html.text, "html.parser")
            htmlContent=Transfer.toUtf8(html.text)
            urllist.append(self.__matchUrl(htmlContent))
        logging.debug("movie info collected")

        rs=[]
        for i in urllist:
            # print(i)
            for j in i:
                rs.append(j)
        # print("rs->")
        # print(rs)
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
        # logging.debug("html:%s"%(Transfer.toUtf8(html.text)))
        bsobj=BeautifulSoup(Transfer.toUtf8(html.text), "html.parser")
        lst=[]
        for i in bsobj.find_all('a',{'target':'_self'}):
            rs=self.__matchMagnet(str(i))
            if rs!='':
                tmp={'name':i.get_text(),'thunderLink':rs}
                logging.debug("magnet:%s"%(tmp))
                lst.append(tmp)
        return lst

    def __matchUrl(self,html):
        pattern=re.compile(r'http://www\.loldytt\.com/.*/.*/">.+</a>')
        urlPattern=re.compile(r'http://www\.loldytt\.com/[\w|\d]+/[\w|\d]+/')
        match=pattern.findall(html)

        lst=[]
        for i in match:
            tmpstr=i.replace('</a>','')
            try:
                url=urlPattern.match(tmpstr).group()
            except Exception as e:
                logging.warning("无法解析:%s"%tmpstr)
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
        logging.info("spider running...")
        rs=spider.search(movie)
        # print(rs)
        for index,item in enumerate(rs):
            logging.debug('%d|%s|%s'%(index,item['name'],item['url']))
            print('%d|%s|%s'%(index,item['name'],item['url']))

    def getBtlink(self,url):
        spider=Spider()
        rs=spider.getMagnet(url)
        # for item in rs:
        #     print(item['thunderLink'])
        #     return
        print(rs[0]['thunderLink'])


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
        try:
            return text.encode('gb2312')
        except Exception as e:
            logging.warning(e)
            return ""
        

    def toUtf8(text):
        try:
            return text.encode('ISO-8859-1').decode('gb2312')
            # return text.encode('ISO-8859-1').decode('utf-8')
            # return text.encode('ISO-8859-1').decode('utf-8')
        except Exception as e:
            logging.warning(e)
            return text
        

def isUrlCode(code):
    #有问题
    match=re.match(r'^[%\w]+$',code)
    if match:
        return True
    else:
        return False

if __name__ == '__main__':
    # click()
    if len(sys.argv)==2:
        #电影名
        movie=sys.argv[1]
        if movie=='test':
            te=test()
            te.printMovieInfo()
            # te.test_isUrlCode()
        else:
            movie=urllib.parse.unquote(movie)
            logging.info("start search, movie:%s"%(movie))
            movieHandler=Movie()
            movieHandler.getMovie(movie)
            logging.info("finish search...")
    elif len(sys.argv)==3:
        #url bt
        url=sys.argv[1]
        cmd=sys.argv[2]
        logging.info("start get btlink: targetUrl->%s  cmd->%s"%(url,cmd))
        movieHandler=Movie()
        movieHandler.getBtlink(url)


    
