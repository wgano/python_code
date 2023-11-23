import requests
import csv
import re
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import asyncio
import aiofiles


# cookies={"auth_time":"1691209472604","usermain":"zlibrary-global.se","domainsNotWorking":"zlibrary-asia.se","remix_userid":"33721248","remix_userkey":"8b1ee04c10498296fdee31d1eed3cee3"}
async def sub_url(bookname,n, url, head, cookies_, pages, write):
    obj2 = re.compile('<div class="buttons">.*?<a href="(?P<resource>.*?)"  class="icons" target="_blank">', re.S)
    async with aiohttp.ClientSession(cookies=cookies_) as session:
        async with session.get(url, headers=head) as res:
            sub = await res.text()
            #             print(sub)
            filter_ = obj2.finditer(sub)
            for j in filter_:
                t = j.group("resource")
            dic = {}
            dic['name'] = n.group("name")
            dic['publisher'] = n.group("publisher")
            dic['author'] = n.group("author")
            dic['ram'] = n.group("ram")
            dic['resource'] = t
            if write:
                async with aiofiles.open(bookname + f"sum of {pages}P" + ".csv", mode="a", encoding="utf-8") as f:
                    cs = csv.writer(f)
                    cs.writerow(dic.values())
                    print(n.group("name") + "\n读写成功!\n")
            else:
                print(n.group("name") + "\t" + n.group("ram") + "\n" + n.group("publisher") + "\t" + n.group(
                    "author") + "\n资源链接:\n" + t + "\n")


async def catch(bookname, url, cookies, header, page, write, pages):
    #     ?usermain=zlibrary-global.se&token=33721786|b13c1cffd5fc69ad5db39645bab77fb5

    domain = url  # +"?usermain=zlibrary-global.se&token="+userid+"|"+userkey
    cookies_ = cookies
    book = bookname
    url_ = domain + "s/" + book + "?page=" + str(page)
    head = header
    res = requests.get(url_, headers=head, cookies=cookies_)
    al = res.text
    #     print(al)
    res.close()
    obj1 = re.compile(
        '<h3 itemprop="name">.*?<a href="(?P<child_url>.*?)" style="text-decoration: underline;">(?P<name>.*?)</a>.*?title="Publisher">(?P<publisher>.*?)</a></div>.*?<div class="authors">.*?">(?P<author>.*?)</a>.*?<div class="property_value.*?<div class="property_value.*?<div class="property_value ">(?P<ram>.*?)</div></div>',
        re.S)

    filter1 = obj1.finditer(al)
    t = []
    for i in filter1:
        child_url = domain + i.group("child_url")
        t.append(
            asyncio.create_task(sub_url(bookname=bookname,n=i, url=child_url, head=head, cookies_=cookies_, pages=pages, write=write)))
    await asyncio.wait(t)


def catch_pool(bookname, url, cookies, header, page, write, pages):
    #     ?usermain=zlibrary-global.se&token=33721786|b13c1cffd5fc69ad5db39645bab77fb5

    domain = url  # +"?usermain=zlibrary-global.se&token="+userid+"|"+userkey
    cookies_ = cookies
    book = bookname
    url_ = domain + "s/" + book + "?page=" + str(page)
    head = header
    res = requests.get(url_, headers=head, cookies=cookies_)
    al = res.text
    #     print(al)
    res.close()
    obj1 = re.compile(
        '<h3 itemprop="name">.*?<a href="(?P<child_url>.*?)" style="text-decoration: underline;">(?P<name>.*?)</a>.*?title="Publisher">(?P<publisher>.*?)</a></div>.*?<div class="authors">.*?">(?P<author>.*?)</a>.*?<div class="property_value.*?<div class="property_value.*?<div class="property_value ">(?P<ram>.*?)</div></div>',
        re.S)
    obj2 = re.compile('<div class="buttons">.*?<a href="(?P<resource>.*?)"  class="icons" target="_blank">', re.S)
    filter1 = obj1.finditer(al)
    for i in filter1:
        child_url = domain + i.group("child_url")
        child_res = requests.get(child_url, headers=head, cookies=cookies_)
        sub = child_res.text
        #         print(child_url,sub)
        child_res.close()
        filter2 = obj2.finditer(sub)
        for j in filter2:
            t = j.group("resource")
        if write:
            f = open(bookname + f"sum of {pages}P" + ".csv", mode="a", encoding="utf-8")
            cs = csv.writer(f)
            dic = {}
            dic['name'] = i.group("name")
            dic['publisher'] = i.group("publisher")
            dic['author'] = i.group("author")
            dic['ram'] = i.group("ram")
            dic['resource'] = t
            cs.writerow(dic.values())
            print(i.group("name") + "\n读写成功!\n")

        else:
            print(i.group("name") + "\t" + i.group("ram") + "\n" + i.group("publisher") + "\t" + i.group(
                "author") + "\n资源链接:\n" + t + "\n")


def catch_book(bookname, url="https://k.zlib.lol/",
               cookies={"auth_time": "1691209472604", "usermain": "zlibrary-global.se",
                        "domainsNotWorking": "zlibrary-asia.se", "remix_userid": "33721248",
                        "remix_userkey": "8b1ee04c10498296fdee31d1eed3cee3"}, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"},
               page=1, write=False, pool=0, pages=1):
    if pool:
        with ThreadPoolExecutor(pool) as th:
            for i in range(1, pages + 1):
                th.submit(catch_pool, bookname=bookname, url=url, cookies=cookies, header=headers, page=i, write=write,
                          pages=pages)
        print("allover!")
    else:
        asyncio.run(
            catch(bookname=bookname, url=url, cookies=cookies, header=headers, page=page, write=write, pages=pages))
        print("oneover!")
    # bookname是要找的书名,url是爬取的目标网站,cookies和headers是链接上网址的必备数据,不必管他,page是搜索第几页,write是是否保存为文件


# pool是是否使用多线程,pool的数也就代表了多线程数,pages是和多线程一起用的,是指要爬取多少页
def download(resource):
    rep = requests.get(resource)
    name = resource.split("filename=")
    with open(name[-1], mode="wb") as f:
        f.write(rep.content)
    print("over")


# catch_book("人工智能")#,write=True,pool=50,pages=10
# 抓取搜索"人工智能"得到的书籍,最多10个页面的内容,用50线程池,并记录在一个csv文件中
if __name__ == "__main__":
    catch_book("你好世界",pool=50,pages=10)