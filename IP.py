from lxml import etree
import requests
from bs4 import BeautifulSoup
import os
import re
import time
import random
#定义的一些全局变量
url='https://www.toolbaba.cn/ip?p='             #目标网站
basePath = os.getcwd()                                         #当前程序所在的路径
userAgentList = [                                              #user-agent列表
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3823.400 QQBrowser/10.7.4307.400",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4315.4 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
]
timeout = 10                                                    #连接超时时间
ipList = {}                                                     #这里我把这两个列表也直接全局变量了
okList = {}       
#获取网页html代码部分
def get_one_page(url): 
    global timeout
#     time.sleep(5)                                             #睡眠1秒，避免频繁范围
    headers={                                                   #在请求头中加入user-agent参数，通过random库，
        'User-Agent':random.choice(userAgentList),              #随机选取上面user-agent列表中的一条user-agent
    }
    response=requests.get(                                      #发起请求
        url,                                                    #目标网站
        headers=headers,                                        #请求头
#         timeout=timeout,                                      #超时时间
#         verify=False,                                         #不检测ssl证书
    )
    if response.status_code==200:                               #响应状态码为200的情况，表示访问成功
        response.close()                                        #按网上的方法来的，避免连接太多
        return response.text                                    #返回目标网站的html代码
    return None
#解析HTML
def parse_one_page(html):                                       #解析html部分
    global ipList
    soup=BeautifulSoup(html,'lxml')                             #用beautifulsoup进行解析
    [s.extract() for s in soup.find_all("th",{"colspan": "10"})]  
    table = soup.find_all(class_="table table-bordered table-hover")[0]    #选取html代码中class为table table-bordered table-striped的第一个标签
#     print(table)
    trList = table.select("tr")                                 #再选取其中标签为tr的所有标签
#     print(trList)
    for i in range(len(trList)):                                #循环获取tr的标签列表
        if (i != 0):                                            #由于第一个tr是表头中的tr，所以我们要去掉第一个tr，所以i要不等于0
            tdList = trList[i].select("td")                     #选取当前tr标签中的td标签
            try:
             ip = tdList[0].next_element+":"+tdList[1].next_element   #通过分析html代码我们可以知道，第一个和第二个td是我们需要的ip和端口号
             print(ip)
             with open('ip.txt', 'a') as f:                     #写入文件
                f.write(ip + "\n")
             aDict = {"https":ip}                                #将ip做成一个字典（其实这么做是错的，字典的key只能唯一，所以会覆盖之前的ip）
             ipList.update(aDict)                                #将aDict存进ipList
            except:
                print('抓取失败')
    return ipList           
#主函数
def main():
    global url
    for i in range(10):                                       #通过循环取得一个数字i
        html=get_one_page(url+str(i))                       #因为循环是从0开始的，并且转换成str类型添加在url末尾
        parse_one_page(html)
main()
