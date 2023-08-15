from _util import azure_sku_price
from pprint import pprint


if __name__ == "__main__":

    import sys, os
    _query = sys.argv[1]
    _ans, _steps = azure_sku_price(_query)
    print(f"> ans: '{_ans}'")
    print(f"> steps: '{_steps}'")


# python get-sku_price.py "General Purpose Serverless Standard-series (Gen5) compute, 8 vCore"
# python get-sku_price.py "Business critical, DC-series, Hour, 4 vCore"
# python get-sku_price.py "General Purpose Fsv2-series hardware, 18 vCore"
