import sys
import requests
from bs4 import BeautifulSoup

# with open("t5.disk.html", "r") as rf:
#     soup = BeautifulSoup(rf, "html.parser")  # 解析响应
#     links = soup.find_all("a")  # 找到所有的<a>标签
#     for link in links:  # 遍历链接
#         # print(link)
#         print(link["href"]) # 打印链接地址

with open(sys.argv[1], "r") as rf:
    soup = BeautifulSoup(rf, "html.parser")  # 解析响应
    links = soup.find_all("a")  # 找到所有的<a>标签
    for link in links:  # 遍历链接
        # print(link)
        print(link["href"]) # 打印链接地址
