import requests
import csv
import re

def catch_book(bookname,url="https://k.zlib.lol/",cookies={"remix_userid":"33721901","remix_userkey":"394c45c790d6afab13ab6fd550760078","auth_time":"1691072411821","usermain":"zlibrary-global.se","domainsNotWorking":"zlibrary-asia.se"},headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"},page=1,write=False):
    domain=url
    cookies_=cookies
    book = bookname
    url_ = domain+"s/"+book+"?page="+str(page)

    head = headers
    

    res = requests.get(url_,headers = head,cookies=cookies_)
    al = res.text
    # print(al)
    res.close()
    obj1 = re.compile('<h3 itemprop="name">.*?<a href="(?P<child_url>.*?)" style="text-decoration: underline;">(?P<name>.*?)</a>.*?title="Publisher">(?P<publisher>.*?)</a></div>.*?<div class="authors">.*?">(?P<author>.*?)</a>',re.S)
    obj2 = re.compile('<div class="buttons">.*?<a href="(?P<resource>.*?)"  class="icons" target="_blank">',re.S)
    filter1 = obj1.finditer(al)
    for i in filter1:
        child_url = domain+i.group("child_url")
        child_res = requests.get(child_url,headers = head,cookies=cookies_)
        sub = child_res.text
        child_res.close()
        filter2 = obj2.finditer(sub)
    
        for j in filter2:
            t=j.group("resource")
        if write:
            f = open(bookname+".csv",mode = "a",encoding="utf-8")
            cs = csv.writer(f)
            dic = {}
            dic['name']=i.group("name")
            dic['publisher']=i.group("publisher")
            dic['author']=i.group("author")
            dic['resource']=t
            cs.writerow(dic.values())
            print(i.group("name")+"\t读写成功")
    f.close()
    print("over!")

catch_book("高等数学",write=True)


def download(resource):
    rep = requests.get(resource)
    name = resource.split("filename=")
    with open(name[-1],mode="wb") as f:
        f.write(rep.content)
    print("over")


download("https://ipfs.cat/xipfs/?cid=QmPdGJzr1okMzEAt7hhV557cidAVA3YqhFFkZ2v3kucbY1&blake2b=bafykbzacecmxfiobjsso4vszfvierr5fodh7e5gaxj5mlydbdfxzyck7lgozi&filename=高等数学习题全解指南同济第7版.上册 (同济大学数学系) (Z-Library).pdf")
