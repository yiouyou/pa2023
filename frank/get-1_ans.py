from _util import get_ans_from_qlist


if __name__ == "__main__":

    import os, sys, json
    _json = "azure_service.json"
    ##### get service
    _dir = sys.argv[1]
    _dir_s = _dir.split("_")
    _service = " ".join(_dir_s[1:-1])
    print(_service)
    ##### get ans
    get_ans_from_qlist(_json, _dir, _service)
    # python get-1_ans.py tmp_azure_managed_disk_1690529169
    # python get-1_ans.py tmp_azure_sql_database_1690531985
    # python get-1_ans.py tmp_azure_sql_managed_instance_1690535170
    # python get-1_ans.py tmp_azure_static_web_apps_1690531612

