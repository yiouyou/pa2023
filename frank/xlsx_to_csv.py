import pandas as pd
import sys
from pprint import pprint
_fn = sys.argv[1]

#0 currencyCode
#1 tierMinimumUnits
#2 retailPrice
#3 unitPrice
#4 armRegionName
#5 location
#6 effectiveStartDate
#7 meterId
#8 meterName
#9 productId
#10 skuId
#11 productName
#12 skuName
#13 serviceName
#14 serviceId
#15 serviceFamily
#16 unitOfMeasure
#17 type
#18 isPrimaryMeterRegion
#19 armSkuName
#20 reservationTerm
#21 term

_col = ["currencyCode", "tierMinimumUnits", "retailPrice", "unitPrice", "armRegionName", "location", "effectiveStartDate", "meterId", "meterName", "productId", "skuId", "productName", "skuName", "serviceName", "serviceId", "serviceFamily", "unitOfMeasure", "type", "isPrimaryMeterRegion", "armSkuName", "reservationTerm", "term"]

_h = {}

df = pd.read_excel(_fn, header=0)
df = df[df['serviceName']=='SQL Database']

_info = ["productName", "skuName", "meterName", "serviceName", "serviceFamily", "unitOfMeasure", "type", "armSkuName", "reservationTerm", "term"]
# _info = ["productName", "skuName", "meterName", "serviceName", "serviceFamily", "unitOfMeasure", "type", "reservationTerm", "term"]

_info_d = []
for index, row in df.iterrows():
    _str = []
    for i in _info:
        if not pd.isna(row[i]):
            _str.append(row[i])
    _info_str = ", ".join(_str)
    # print(_info_str)
    _info_d.append(_info_str)

df["_info"] = _info_d

df["r_u"] = df["retailPrice"] - df["unitPrice"]
print(df["r_u"].sum())

out = df[["_info", "unitPrice", "skuId", "meterId"]]
out.to_csv('_info_unitPrice_all.csv', index=False)
# out.to_csv('_info_unitPrice_noArmSKU.csv', index=False)
