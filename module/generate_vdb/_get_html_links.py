def get_html_links(_html):
    from bs4 import BeautifulSoup
    _link = {}
    _href = []
    with open(_html, "r") as rf:
        soup = BeautifulSoup(rf, "html.parser")  # 解析响应
        links = soup.find_all("a")  # 找到所有的<a>标签
        for i in links:  # 遍历链接
            # print(i)
            i_href = i["href"]
            # print(i_href) # 打印链接地址
            _href.append(i_href)
            _link[i_href] = 1
    _links = sorted(_link.keys())
    # print(f"{len(_href)} -> {len(_links)}")
    return _links


if __name__ == "__main__":

    import os
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _pa_path = _pwd.parent.parent.parent
    _html = os.path.join(_pa_path, 'test/t5.webapp.html')
    # print(_html)
    _links = get_html_links(_html)
    for i in _links:
        print(i)
    # print(_links)
    # print(len(_links))

