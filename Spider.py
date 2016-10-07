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
        param={'keyword':self.toGb2312(movie)}
        url='http://so.loldytt.com/search.asp'
        html=requests.post(url,params=param)
        # html=requests.post("http://so.loldytt.com/search.asp?keyword=%B0%A2%B8%CA")
        bsobj=BeautifulSoup(html.text)
        htmlContent=self.toUtf8(html.text)
        urldic=self.matchUrl(htmlContent)
        for i in urldic:
            if i['name']==movie:
                return i
        return urldic

    def toGb2312(self,text):
        return text.encode('gb2312')

    def toUtf8(self,text):
        return text.encode('ISO-8859-1').decode('gb2312')

    def matchMagnet(self,text):
        pattern=re.compile(r'thunder:\/\/[A-Za-z0-9\+\/=]*')
        match=pattern.findall(text)
        print(match)
        if match:
            return match[0]
        else:
            return ''

    def getMagnet(self,url):
        html=requests.get(url)
        bsobj=BeautifulSoup(self.toUtf8(html.text))
        lst=[]
        for i in bsobj.find_all('a',{'target':'_self'}):
            print(i.get_text())
            rs=self.matchMagnet(str(i))
            if rs!='':
                lst.append({'name':i.get_text(),'thunderLink':rs})
        print(lst)
        return lst

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

class test_spider:
    def test_matchMagnet(self,text):
        sp=Spider()
        tt='<a href="thunder://QUFmdHA6Ly9keTpkeUB4bGEueHVuYm8uY2M6MTAzNjgvW9G4wNfPwtTYd3d3Llh1bkJvLkNjXbCiuMrV/bSrQkQxMDI0uN/H5dbQ06LLq9fWLnJtdmJaWg==" title="阿甘正传BD1024高清中英双字" target="_self">阿甘正传BD1024高清中英双字</a>'
        print(spider.matchMagnet(tt))

if __name__ == '__main__':
    spider=Spider()
    rs=spider.search('美国恐怖故事第二季')
    print(rs)
    spider.getMagnet(rs['url'])
    # bthtml=requests.get(rs['url'])
    # print(spider.toUtf8(bthtml.text))
    # print(spider.matchMagnet(bthtml.text))
    
