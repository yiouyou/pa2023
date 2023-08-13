from _util import get_sku_price, get_closest
from pprint import pprint


if __name__ == "__main__":

    import sys, os
    _query = sys.argv[1]
    _top_info, _price = get_sku_price(_query)
    print(f"\n{_query}\n")
    _n = 0
    for i in _top_info:
        _n += 1
        print(f"{_n}. {i}")
    _r, _r_step = get_closest(_query, _top_info)
    print()
    print(_r)
    print(_r_step)
    _s = _top_info[int(_r[0].strip())-1]
    print(f"\n${_price[_s]}, '{_s}'")


# python get-sku_price.py "General Purpose Serverless Standard-series (Gen5) compute, 8 vCore"
# python get-sku_price.py "Business critical, DC-series, Hour, 4 vCore"
# python get-sku_price.py "General Purpose Fsv2-series hardware, 18 vCore"
