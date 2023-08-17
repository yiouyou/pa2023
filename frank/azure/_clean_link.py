import sys
_f = sys.argv[1]
# print(_f)

with open(_f, 'r', encoding='utf-8') as rf:
    _li = rf.readlines()

_c = ["view=azuresql-db", "view=azuresql-mi", "view=azuresql-vm"]

_link = []
for i in _li:
    _i = i.strip()
    _link.append(_i)

_cc = {}
_u = []
import re
for i in _link:
    _n = 0
    for j in _c:
        # print(j, i)
        if j in i:
            # print(i, j)
            _l = re.sub(r"{}".format(j), '', i)
            # print(_l)
            # print()
            _jj = j.split('-')
            if _jj[-1] in _cc.keys():
                _cc[_jj[-1]][_l] = 1
            else:
                _cc[_jj[-1]] = {}
                _cc[_jj[-1]][_l] = 1
            _n += 1
    if _n == 0:
        _u.append(i)
# print(len(_u))

for i in _u:
    print(i)
# print()
# for i in _cc:
#     for j in _cc[i]:
#         print(i, j)
# print()
_uu = {}
_cc_keys = _cc.keys()
for i in _cc:
    for j in _cc[i]:
        _n = 0
        for k in _cc_keys:
            if i != k:
                # print(i, k, j)
                # print(_cc[k].keys())
                if j in _cc[k].keys():
                    _n += 1
        # print(_n, j)
        if _n == 0:
            jj = f"{j}view=azuresql-{i}"
            # print(jj)
            _uu[jj] = 1
        else:
            # print(j)
            _uu[j] = 1
# print(len(_uu.keys()))



for i in _uu.keys():
    # print(i)
    if re.search(r'\?$', i):
        m = re.search(r'(.*)\?$', i)
        print(m.group(1))
    elif re.search(r'\&$', i):
        m = re.search(r'(.*)\&$', i)
        print(m.group(1))
    else:
        print(i)

