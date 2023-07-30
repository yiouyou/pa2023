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
    # if not _item:
    #     print("\n\n##############################")
    #     print(_ans)
    # print(_item)
    return _item


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
    print(_ans)
    _item = parse_to_item(_ans)
    print(f"\n----------\n{_q}\n{_item}\n----------\n")
    return _item


def what_and_stepbystep_explanation(_topic, _dj, _service):
    _list = []
    _q0 = f"How many {_topic} does {_service} have, and what are they? Please output in Numbered List."
    _list.append(_q0)
    _item = qa_and_parse_to_item(_q0, _dj, _service)
    if _item:
        for i in _item:
            _qi = ""
            if _topic in ["performance metrics"]: # "pricing options"
                _qi = f"Can you provide a step-by-step explanation of how to use the {i} as one of {_topic}?"
            elif _topic in ["cost drivers", "pricing options"]:
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


def get_ans_from_qlist(_qlist, _dir, _dj, _service):
    _qlist_str = "\n".join(_qlist)
    writeF(_dir, '_qlist', _qlist_str)
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _pa_path = _pwd.parent.parent
    sys.path.append(str(_pa_path))
    from module.query_vdb import qa_faiss_multi_query
    from dotenv import load_dotenv
    load_dotenv()
    import time
    _vdb = _dj[_service]['vdb']
    _ans = []
    for i in _qlist:
        print(f">>> {i}")
        _q = f"{i} Please output in concise English."
        i_ans, i_step = qa_faiss_multi_query(_q, _vdb)
        writeF(_dir, '_ans_/_ans_'+i.replace("?", ""), i_ans)
        writeF(_dir, '_step_/_step_'+i.replace("?", ""), i_step)
        time.sleep(4)
        _ans.append(i_ans)
    _ans_str = ""
    for i in range(len(_qlist)):
        _ans_str += f"## {_qlist[i]}\n\n" + f"{_ans[i]}\n\n"
    writeF(_dir, '_ans', _ans_str)


def del_files(_dir):
    import os
    import glob
    files = glob.glob(_dir)
    for f in files:
        os.remove(f)


if __name__ == "__main__":

    import os, sys, json
    ##### get json
    _json = sys.argv[1]
    _service = sys.argv[2]
    _dir = sys.argv[3]
    _f_qlist = f"{_dir}/_qlist" 
    _dir_ans_ = f"{_dir}/_ans_"
    _dir_step_ = f"{_dir}/_step_"
    del_files(_dir_ans_)
    del_files(_dir_step_)
    with open(_json, 'r', encoding='utf-8') as jf:
        _dj = json.loads(jf.read())
    ##### get qlist
    with open(_f_qlist, 'r', encoding='utf-8') as qf:
        _line = qf.readlines()
    _qlist = [i.strip() for i in _line]
    ##### get ans
    get_ans_from_qlist(_qlist, _dir, _dj, _service)
    # python 1_get_ans_from_qlist.py azure_service.json "azure managed disk" tmp_azure_managed_disk_1690529169
    # python 1_get_ans_from_qlist.py azure_service.json "azure sql database" tmp_azure_sql_database_1690531985
    # python 1_get_ans_from_qlist.py azure_service.json "azure sql managed instance" tmp_azure_sql_managed_instance_1690535170
    # python 1_get_ans_from_qlist.py azure_service.json "azure static web apps" tmp_azure_static_web_apps_1690531612

