from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as Soup
import re
# from package import function as alias
import requests
import pandas as pd

 

def getIframeUrl(url):
    try:
        html = urlopen(url)
    except HTTPError as e:        print(e)
     
    except URLError:        print("Server down or incorrect domain")
     
    else:             res = BeautifulSoup(html.read(), "html5lib")
     
    tags = res.findAll("iframe")
    iframeUrls=[] 
    for tag in tags:
        url_tag = tag['src']
        if str(url_tag[0:4] ) !="http":
            url_tag = "https:"+url_tag
        
        print(url_tag ) #URl of iframe ready for scraping
        iframeUrls.append(url_tag)
        #iframeUrls.append("https:"+tag['src'])
    print("iframe URL inside getIframeUrl",  iframeUrls)
    return iframeUrls 


def getHashTagedVal(source):
    req = requests.get(source)
    reqData = str(req)
    with open("output_req.txt","w") as f1:
        f1.write(reqData)
    print("req : ",req,type(req))
    
    content = Soup(req.text, 'html.parser')
    content = str(content)
    #print("content data",type(content),content)
    webPageDataAsBsObj = Soup(content,"html")
    print("webPageDataAsBsObj", webPageDataAsBsObj)
    print(type(webPageDataAsBsObj))

    return webPageDataAsBsObj 

def findUrlList():
    
    df =  pd.read_csv("shop.csv",encoding='utf-8')
    df.to_csv("output.csv" )

    #urlList = df.iloc[:,1:2]
    #urlList = df[['Web Site']].tolist()
    urlList = df['Web Site'].values
    urlList= urlList[1:] 
    #0,9
    
    print(urlList)
    
    
    return urlList

if __name__ == "__main__":
    print("Atul")
    #functionToprocessWebsite(SOURCE)
    
    print("completed the execution")
    
    urlList= findUrlList()#["https://www.runinrabbit.com/"]
    #urlList= ["runinrabbit.com/"]
     
    print("got the list")  
    i=0
    for url in urlList:
        
        url = "https://www."+url
        print("url number ", i)   
        i +=1
        print("url found ", url)
        
        if url[0:11] != "https://www":
            continue
        iframeUrlList = getIframeUrl(url)
        print("iframeUrlList ", iframeUrlList)

        
        for iframeUrl in iframeUrlList:
            webPageDataAsBsObj = getHashTagedVal(iframeUrl)
            data = str(webPageDataAsBsObj)
            print("iframe Url ",data)
            print("********************************************************************")
            print("type(data) ", type(data))
            if iframeUrl[0:11] != "https://www":
                continue
            
        
            tags = re.findall(r"(?<!\w)#\w+", data)
            tagStr=""
            for tag in tags:
                tagStr += tag+", "
            outPutFileName = url.split('/')[2].split('.')[1] +str(i)+"__output_iframe.txt"
            with open(outPutFileName,"w",encoding="utf-8") as f1:
                f1.write(tagStr)
            
        
     