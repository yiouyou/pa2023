import sys
from pathlib import Path
from pprint import pprint
_pwd = Path(__file__).absolute()
_pa_path = _pwd.parent.parent
# print(_pa_path)
sys.path.append(str(_pa_path))
# pprint(sys.path)
from module.query_vdb import qa_faiss_multi_query
from dotenv import load_dotenv
load_dotenv()

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

_service = 'SQL managed instance' # 'managed disk', 'SQL database', 'SQL managed instance', 'static web apps'
_vdb = 'azure_sql_mi' # 'azure_vm', 'azure_sql_db', 'azure_sql_mi', 'azure_webapps'

##### generate dir
import os
from module.util import timestamp_now
_ts = f"./tmp_sql-mi_1689936595/"
# if not os.path.exists(_ts):
#     os.makedirs(_ts)

##### 3) get all ans from question list
import time
_qlist = readF(_ts, '_ans2+').split("\n")
# print(_qlist)
_ans3 = []
for i in _qlist:
    i_ans, i_step = qa_faiss_multi_query(i, _vdb)
    writeF(_ts, '_ans3+_'+i.replace("?", ""), i_ans)
    writeF(_ts, '_step3+_'+i.replace("?", ""), i_step)
    time.sleep(5)
    _ans3.append(i_ans)

_ans3_str = ""
for i in range(len(_qlist)):
    _ans3_str += f"## {_qlist[i]}\n\n" + f"{_ans3[i]}\n\n"
writeF(_ts, '_ans3+', _ans3_str)

# _ans3_str = ""
# for i in _qlist:
#     i_ans = '_ans3_/_ans3_'+i.replace("?", "")
#     _f = readF(_ts, i_ans)
#     # print(_f)
#     _ans3_str += f"## {i}\n\n" + f"{_f}\n\n"
# writeF(_ts, '_ans3', _ans3_str)
