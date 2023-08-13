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


# python get-sku_price.py tmp_sku_sql_pool 'General_Purpose_service_tier_standard-series_(Gen5)'
# python get-sku_price.py tmp_sku_sql_pool GP_DC-series_hardware
# python get-sku_price.py tmp_sku_sql_pool Fsv2-series_hardware
# python get-sku_price.py tmp_sku_sql_pool 'Business_Critical_service_tier_standard-series_(Gen5)'
# python get-sku_price.py tmp_sku_sql_pool M-series_hardware
# python get-sku_price.py tmp_sku_sql_pool BC_DC-series_hardware
# python get-sku_price.py tmp_sku_sql_pool Gen5_compute_generation

# python get-sku_price.py tmp_sku_sql_pool Basic_elastic_pool_limits
# python get-sku_price.py tmp_sku_sql_pool Premium_elastic_pool_limits
# python get-sku_price.py tmp_sku_sql_pool Standard_elastic_pool_limits
# python get-sku_price.py tmp_sku_sql_pool Database_properties_for_pooled_databases
# python get-sku_price.py tmp_sku_sql_pool Tempdb_sizes

