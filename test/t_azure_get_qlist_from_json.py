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
        m1 = re.search(r"^\d+\. (.+): ", i, re.DOTALL)
        if m1 is not None:
            m1 = m1.group(1)
            if ' - ' in m1:
                m2 = m1.split(' - ')
                _item.append(m2[-1].strip())
            else:
                _item.append(m1.strip())
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
    # print(_ans)
    _item = parse_to_item(_ans)
    # print(_item)
    return _item


def what_and_stepbystep_explanation(_topic, _dj, _service):
    _list = []
    _q0 = f"What are the {_topic} of {_service}?"
    _list.append(_q0)
    _item = qa_and_parse_to_item(_q0, _dj, _service)
    if _item:
      for i in _item:
          _qi = f"Can you provide a step-by-step explanation of how to use the {i} as one of {_topic}?"
          _list.append(_qi)
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
    _module_path = _pwd.parent.parent
    sys.path.append(str(_module_path))
    from module.query_vdb import qa_faiss_multi_query
    from dotenv import load_dotenv
    load_dotenv()
    import time
    _vdb = _dj[_service]['vdb']
    _ans = []
    for i in _qlist:
        i_ans, i_step = qa_faiss_multi_query(i, _vdb)
        writeF(_dir, '_ans_/_ans_'+i.replace("?", ""), i_ans)
        writeF(_dir, '_step_/_step_'+i.replace("?", ""), i_step)
        time.sleep(4)
        _ans.append(i_ans)
    _ans_str = ""
    for i in range(len(_qlist)):
        _ans_str += f"## {_qlist[i]}\n\n" + f"{_ans[i]}\n\n"
    writeF(_dir, '_ans', _ans_str)


if __name__ == "__main__":

    import sys
    import json

    _json = sys.argv[1]
    _service = sys.argv[2]
    # _service = "azure sql managed instance"

    with open(_json, 'r', encoding='utf-8') as jf:
        _dj = json.loads(jf.read())
    _qlist = qlist_from_json(_dj, _service)
    for i in _qlist:
        print(i)

    import os
    from module.util import timestamp_now
    _ts = timestamp_now()
    _service_str = '_'.join(_service.split(' '))
    _dir = f"tmp_{_service_str}_{_ts}"
    _dir_ans_ = f"{_dir}/_ans_"
    _dir_step_ = f"{_dir}/_step_"
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    if not os.path.exists(_dir_ans_):
        os.makedirs(_dir_ans_)
    if not os.path.exists(_dir_step_):
        os.makedirs(_dir_step_)
    get_ans_from_qlist(_qlist, _dir, _dj, _service)


    # python t_azure_get_qlist_from_json.py t_azure_get_qlist_from_json.json "azure sql managed instance"

