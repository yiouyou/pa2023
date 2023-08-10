from _util import generate_sku


if __name__ == "__main__":

    import sys, os
    _dir = sys.argv[1]
    _fn = sys.argv[2]
    _path = os.path.join(_dir, _fn)
    print(_path)
    with open(_path, 'r', encoding='utf-8') as rf:
      _info = rf.read()
    generate_sku(_info, _dir, _fn)

# python get-sku_table.py tmp_sku_sql_pool 'Business_Critical_service_tier_standard-series_(Gen5)'
# python get-sku_table.py tmp_sku_sql_pool Gen5_compute_generation
# python get-sku_table.py tmp_sku_sql_pool Premium_elastic_pool_limits
# python get-sku_table.py tmp_sku_sql_pool DC-series_hardware
# python get-sku_table.py tmp_sku_sql_pool 'General_Purpose_service_tier_standard-series_(Gen5)'
# python get-sku_table.py tmp_sku_sql_pool Standard_elastic_pool_limits
# python get-sku_table.py tmp_sku_sql_pool Fsv2-series_hardware
# python get-sku_table.py tmp_sku_sql_pool M-series_hardware

