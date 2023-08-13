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
# df.to_excel('_sql_database.xlsx', engine='openpyxl', index=False)
df.to_csv('_sql_database.csv', index=False)

for i in _col:
    if not i in ['retailPrice','unitPrice','effectiveStartDate','meterId','productId','skuId','serviceId',  'currencyCode','tierMinimumUnits','armRegionName','location']:
        _h[i] = df[i].unique()
        # print(f"## {i}")
        # for j in df[i].unique():    
        #     print(j)
    # print()


for i in _h:
    print(f"## {i}")
    for j in _h[i]:
        print(j)
    print("\n")
pprint(sorted(_h.keys()))
