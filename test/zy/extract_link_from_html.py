
def extract_link_from_html(_html, _http, _out):
    import sys
    import requests
    from bs4 import BeautifulSoup
    _link = []
    with open(_html, "r") as rf:
        soup = BeautifulSoup(rf, "html.parser")  # 解析响应
        links = soup.find_all("a")  # 找到所有的<a>标签
        for link in links:  # 遍历链接
            # print(link)
            _url = _http + link["href"]
            print(_url) # 打印链接地址
            _link.append(_url)
    _link_str = "\n".join(_link)
    with open(_out, 'w', encoding='utf-8') as wf:
        wf.write(_link_str)

_gmzy = {
    "gmzy_rm": "https://www.gmzyjc.com/read/rm/",
    "gmzy_kj": "https://www.gmzyjc.com/read/kj/",
    "gmzy_qs": "https://www.gmzyjc.com/read/qs/",
    "gmzy_ql": "https://www.gmzyjc.com/read/ql/",
    "gmzy_bc": "https://www.gmzyjc.com/read/bc/",
    "gmzy_fjx": "https://www.gmzyjc.com/read/fjx/",
    "gmzy_hdnjs": "https://www.gmzyjc.com/read/hdnjs/",
    "gmzy_shl": "https://www.gmzyjc.com/read/shl/",
    "gmzy_jgyl": "https://www.gmzyjc.com/read/jgyl/",
    "gmzy_wbtb": "https://www.gmzyjc.com/read/wbtb/",
    "gmzy_nk": "https://www.gmzyjc.com/read/nk/",
    "gmzy_wk": "https://www.gmzyjc.com/read/wk/",
    "gmzy_fk": "https://www.gmzyjc.com/read/fk/",
    "gmzy_ek": "https://www.gmzyjc.com/read/ek/",
    "gmzy_lzcx": "https://www.gmzyjc.com/read/lzcx/",
    "gmzy_hk": "https://www.gmzyjc.com/read/hk/",
    "gmzy_yk": "https://www.gmzyjc.com/read/yk/",
    "gmzy_gk": "https://www.gmzyjc.com/read/gk/",
    "gmzy_zywx": "https://www.gmzyjc.com/read/zywx/",
    "gmzy_zjs": "https://www.gmzyjc.com/read/zjs/",
    "gmzy_zjz": "https://www.gmzyjc.com/read/zjz/",
    "gmzy_zjx": "https://www.gmzyjc.com/read/zjx/",
    "gmzy_ya": "https://www.gmzyjc.com/read/ya/",
    "gmzy_yjxj": "https://www.gmzyjc.com/read/yjxj/",
    "gmzy_zxyjh": "https://www.gmzyjc.com/read/zxyjh/",
    "gmzy_gbshl": "https://www.gmzyjc.com/read/gbshl/",
    "gmzy_hdnjls": "https://www.gmzyjc.com/read/hdnjls/",
    "gmzy_hdnjsw": "https://www.gmzyjc.com/read/hdnjsw/",
    "gmzy_nj": "https://www.gmzyjc.com/read/nj/",
    "gmzy_pwl": "https://www.gmzyjc.com/read/pwl/",
    "gmzy_fxj": "https://www.gmzyjc.com/read/fxj/",
    "gmzy_mj": "https://www.gmzyjc.com/read/mj/",
}

for i in _gmzy:
    i_html = f"{i}.html"
    i_http = _gmzy[i]
    i_out = f"{i}.link"
    extract_link_from_html(i_html, i_http, i_out)

# python extract_link_from_html.py gmzy_summary.html "https://www.gmzyjc.com/read/rm/" > gmzy_summary.link

