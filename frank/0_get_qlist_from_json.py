def writeF(_dir, _fn, _txt):
    import os
    wfn = os.path.join(_dir, _fn)
    with open(wfn, 'w', encoding='utf-8') as wf:
        wf.write(_txt)


def readF(_dir, _fn):
    import os
    rfn = os.path.join(_dir, _fn)
    with open(rfn, 'r', encoding='utf-8') as rf:
        return rf.read()


def parse_to_item(_ans):
    _item = []
    import re
    _li = _ans.split("\n")
    for i in _li:
        i = i.strip()
        _m = ''
        if ':' in i:
            m1 = re.search(r"^\d+\. (.+)\: ", i, re.DOTALL)
            if m1 is not None:
                _m = m1.group(1)
        elif ']' in i:
            m2 = re.search(r"^\d+\. \[(.+)\]", i, re.DOTALL)
            if m2 is not None:
                _m = m2.group(1)
        else:
            m3 = re.search(r"^\d+\. (.+)", i, re.DOTALL)
            if m3 is not None:
                _m = m3.group(1)
        if _m:
            if ' - ' in _m:
                _ms = _m.split(' - ')
                _item.append(_ms[-1].strip())
            else:
                _item.append(_m.strip())
    if not _item:
        print("\n\n##############################")
        print(_ans)
        exit()
    # print(_item)
    return _item

# _ans = """1. SQL Database - Single database
# 2. SQL Database - Elastic pool"""
# _ans="""1. vCore-based purchasing model: This model allows you to choose the number of vCores, the amount of memory, and the amount and speed of storage. It offers more flexibility and control over resource allocation. You can also use Azure Hybrid Benefit for SQL Server to save costs by leveraging your existing SQL Server licenses.

# 2. DTU-based purchasing model: This model offers a blend of compute, memory, and I/O resources in three service tiers (Basic, Standard, and Premium) to support different database workloads. Each tier has different compute sizes and allows you to add additional storage resources."""
# _ans = """1. [SQL Managed Instance - Single instance](/en-us/pricing/details/azure-sql-managed-instance/single/)
# 2. [SQL Managed Instance - Instance pool](/en-us/pricing/details/azure-sql-managed-instance/pools/)"""
# print(parse_to_item(_ans))
# exit()


def qa_and_parse_to_item(_q, _dj, _service):
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _module_path = _pwd.parent.parent
    sys.path.append(str(_module_path))
    from module.query_vdb import qa_faiss_multi_query
    from dotenv import load_dotenv
    load_dotenv()
    _vdb = _dj[_service]['vdb']
    _ans, _step = qa_faiss_multi_query(_q, _vdb)
    # print(_ans)
    _item = parse_to_item(_ans)
    # print(_item)
    return _item


def what_and_stepbystep_explanation(_topic, _dj, _service):
    _list = []
    _q0 = f"How many {_topic} does {_service} have, and what are they? Please output in Numbered List."
    _list.append(_q0)
    _item = qa_and_parse_to_item(_q0, _dj, _service)
    if _item:
        for i in _item:
            _qi = ""
            if _topic in ["performance metrics", "pricing options"]:
                _qi = f"Can you provide a step-by-step explanation of how to use the {i} as one of {_topic}?"
            elif _topic in ["cost drivers"]:
                _qi = f"What are the best practices for choosing suitable {i} based on usage to save cost?"
            if _qi:
                _list.append(_qi)
            else:
                print("ERROR: wrong topic")
    return _list


def comparison_between_itmes(_c1, _c2, _dj, _service):
    _list = []
    _g = _dj[_service]['qlist'][_c1]['key_concept'][_c2]
    for i in _g:
        i_q0 = f"What are the unique features of '{i}' in {_c2}?"
        i_q1 = f"What are the limitations of '{i}' in {_c2}?"
        i_q2 = f"When should I choose '{i}' in {_c2}?"
        _list.extend([i_q0, i_q1, i_q2])
    for i in range(len(_g)):
        for j in range(i+1, len(_g)):
            print(_g[i], _g[j])
            _gi = f"'{_g[i]}' in {_c2}"
            _gj = f"'{_g[j]}' in {_c2}"
            j_q0 = f"What's the difference between {_gi} and {_gj}?"
            j_q1 = f"When should I choose {_gi} over {_gj}?"
            j_q2 = f"When should I choose {_gj} over {_gi}?"
            _list.extend([j_q0, j_q1, j_q2])
    # print(_list)
    return _list


def qlist_from_json(_dj, _service):
    _d = _dj[_service]['qlist']
    # print(_d)
    _list = []
    for i in _d.keys():
        i_list = what_and_stepbystep_explanation(i, _dj, _service)
        _list.extend(i_list)
        if 'key_concept' in _d[i]:
            _d_kc = _d[i]['key_concept']
            for j in _d_kc.keys():
              # print(i, j)
              if _d_kc[j]:
                  print(j)
                  _compare_list = comparison_between_itmes(i, j, _dj, _service)
                  _list.extend(_compare_list)
              else:
                  print()
                  _qj = f"Can you provide a step-by-step explanation of how the {j} affect the cost of {_service}?"
                  _list.extend([_qj])
        # else:
        #     print(i)
    _qlist = sorted(list(set(_list)))
    return _qlist


if __name__ == "__main__":

    import os, sys, json
    ##### get json
    _json = sys.argv[1]
    _service = sys.argv[2]
    # _service = "azure sql managed instance"
    ##### get qlist
    with open(_json, 'r', encoding='utf-8') as jf:
        _dj = json.loads(jf.read())
    _qlist = qlist_from_json(_dj, _service)
    for i in _qlist:
        print(i)

