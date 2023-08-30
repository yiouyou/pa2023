from _util import qlist_from_json


if __name__ == "__main__":

    import os, sys, json
    from module.util import timestamp_now
    _json = "azure_service.json"
    ##### get service
    _service = sys.argv[1]
    _service_str = '_'.join(_service.split(' '))
    _ts = timestamp_now()
    _dir = f"tmp_{_service_str}_{_ts}"
    if len(sys.argv) == 3:
      _dir = sys.argv[2]
    ##### get qlist
    _qlist = qlist_from_json(_json, _dir, _service)
    print(f"---------- qlist ----------\n")
    for i in _qlist:
        print(i)
    # python get-0_qlist.py "azure sql managed instance"
    # python get-0_qlist.py "azure sql database"
    # python get-0_qlist.py "azure cosmos db"
    # python get-0_qlist.py "azure monitor"
    # python get-0_qlist.py "azure synapse"
    # python get-0_qlist.py "azure app service"
    # python get-0_qlist.py "azure linux virtual machines"
    # python get-0_qlist.py "azure managed disk"
    # python get-0_qlist.py "azure blob storage"
    # python get-0_qlist.py "azure page blobs"
    # python get-0_qlist.py "azure data lake"
    # python get-0_qlist.py "azure databricks"
    # python get-0_qlist.py "azure cache redis"

