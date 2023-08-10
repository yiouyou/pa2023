from _util import extract_table_from_md


if __name__ == "__main__":

    import sys
    _dir = sys.argv[1]
    _fn = sys.argv[2]
    extract_table_from_md(_dir, _fn)

# python get-md_table.py tmp_sku_sql_pool/ ../module/generate_vdb/md_azure_sql_db/0215.md
# python get-md_table.py tmp_sku_sql_pool/ ../module/generate_vdb/md_azure_sql_db/0218.md

