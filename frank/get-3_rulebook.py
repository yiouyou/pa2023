from _util import extract_rulebook


if __name__ == "__main__":

    import os, sys, json
    _json = "azure_service.json"
    ##### get service
    _dir = sys.argv[1]
    _dir_s = _dir.split("_")
    _service = " ".join(_dir_s[1:-1])
    print(_service)
    ##### get rules
    extract_rulebook(_dir, _service)
    # python get-3_rulebook.py tmp_azure_app_service_1691242530
    # python get-3_rulebook.py tmp_azure_blob_storage_1691243666
    # python get-3_rulebook.py tmp_azure_cosmos_db_1691240362
    # python get-3_rulebook.py tmp_azure_data_lake_1691244691
    # python get-3_rulebook.py tmp_azure_linux_virtual_machines_1691243001
    # python get-3_rulebook.py tmp_azure_managed_disk_1691243309
    # python get-3_rulebook.py tmp_azure_monitor_1691240700
    # python get-3_rulebook.py tmp_azure_page_blobs_1691244086
    # python get-3_rulebook.py tmp_azure_sql_database_1691239657
    # python get-3_rulebook.py tmp_azure_sql_managed_instance_1691239129
    # python get-3_rulebook.py tmp_azure_synapse_1691241703
    # python get-3_rulebook.py tmp_azure_databricks_1692241737

