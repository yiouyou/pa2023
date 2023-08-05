import sys
from pathlib import Path
_pwd = Path(__file__).absolute()
_pa_path = _pwd.parent.parent
sys.path.append(str(_pa_path))


def writeF(_dir, _fn, _txt):
    import os
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    wfn = os.path.join(_dir, _fn)
    print(wfn)
    with open(wfn, 'w', encoding='utf-8') as wf:
        wf.write(_txt)


def readF(_dir, _fn):
    import os
    _txt = ""
    rfn = os.path.join(_dir, _fn)
    with open(rfn, 'r', encoding='utf-8') as rf:
        _txt = rf.read()
    return _txt


def _split_item(_str):
    import re
    return re.split(", | and | or ", _str)


def parse_to_item(_ans):
    _item = []
    import re
    _li = _ans.split("\n")
    for i in _li:
        i = i.strip()
        _m = ''
        if '**' in i:
            m = re.search(r"\*\*(.+)\*\*", i, re.DOTALL)
            if m is not None:
                _m = m.group(1)
        else:
            if ':' in i:
                if '[' in i and ']' in i:
                    m1 = re.search(r"^\d+\. [^\:]*\[(.+)\].*\:", i, re.DOTALL) # []在:前
                    if m1 is not None:
                        _m = m1.group(1)
                    else:
                        m2 = re.search(r"^\d+\. ([^\:]+)\:", i, re.DOTALL) # 第一个:, 第二个:可能是https:
                        if m2 is not None:
                            _m = m2.group(1)
                else:
                    m = re.search(r"^\d+\. ([^\:]+)\:", i, re.DOTALL)
                    if m is not None:
                        _m = m.group(1)
            else:
                if '[' in i and ']' in i:
                    m = re.search(r"^\d+\. .*\[(.+)\].*", i, re.DOTALL) # []在:前
                    if m is not None:
                        _m = m.group(1)
                else:
                    m = re.search(r"^\d+\. (.+)", i, re.DOTALL)
                    if m is not None:
                        _m = m.group(1)
        if _m:
            if ' - ' in _m:
                _ms = _m.split(' - ')
                print(_ms[-1])
                _s = _split_item(_ms[-1].strip())
                _item.extend(_s)
            else:
                _s = _split_item(_m.strip())
                _item.extend(_s)
    # if not _item:
    #     print("\n\n##############################")
    #     print(_ans)
    # print(_item)
    return _item
# _ans = """1. SQL Database - Single database
# 2. SQL Database - Elastic pool"""
# print(_ans,"\n")
# print(parse_to_item(_ans),"\n")
# _ans="""1. vCore-based purchasing model: This model allows you to choose the number of vCores, the amount of memory, and the amount and speed of storage. It offers more flexibility and control over resource allocation. You can also use Azure Hybrid Benefit for SQL Server to save costs by leveraging your existing SQL Server licenses.
# 2. DTU-based purchasing model: This model offers a blend of compute, memory, and I/O resources in three service tiers (Basic, Standard, and Premium) to support different database workloads. Each tier has different compute sizes and allows you to add additional storage resources."""
# print(_ans,"\n")
# print(parse_to_item(_ans),"\n")
# _ans = """1. [SQL Managed Instance - Single instance](/en-us/pricing/details/azure-sql-managed-instance/single/)
# 2. [SQL Managed Instance - Instance pool](/en-us/pricing/details/azure-sql-managed-instance/pools/)"""
# print(_ans,"\n")
# print(parse_to_item(_ans),"\n")
# _ans = """1. **Disk IO, throughput and queue depth metrics:** These metrics allow you to see the storage performance from the perspective of a disk and a virtual machine.
# 2. **Disk bursting metrics:** These metrics provide observability into the bursting feature on premium disks."""
# print(_ans,"\n")
# print(parse_to_item(_ans),"\n")
# _ans = "1. Single Instance Pricing: This is the cost for a single SQL Managed Instance. The price varies based on the service tier and compute size you choose. For detailed pricing, you can visit the [Azure SQL Managed Instance single instance pricing page](https://azure.microsoft.com/pricing/details/azure-sql-managed-instance/single/)."
# print(_ans,"\n")
# print(parse_to_item(_ans),"\n")
# _ans = """1. **Disk IO, throughput and queue depth metrics** - These metrics allow you to see the storage performance from the perspective of a disk and a virtual machine.
# 2. **Disk bursting metrics** - These are the metrics provide observability into the bursting feature on premium disks."""
# print(_ans,"\n")
# print(parse_to_item(_ans),"\n")
# _ans = """1. [SQL Database - Single database](/en-us/pricing/details/azure-sql-database/single/): This option provides pricing for a single Azure SQL database. The cost depends on the compute tier and storage capacity you choose.
# 2. [SQL Managed Instance - Single instance](/en-us/pricing/details/azure-sql-managed-instance/single/): This pricing option is for a single instance of SQL Managed Instance. The cost varies based on the compute tier and storage capacity you select."""
# print(_ans,"\n")
# print(parse_to_item(_ans),"\n")
# exit()


def qa_weblink(_q, _weblink):
    _ans, _step = "", ""
    import os, re
    from langchain.chat_models import ChatOpenAI
    from langchain.llms import OpenAI
    from langchain.chains.question_answering import load_qa_chain
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.vectorstores import Chroma
    from langchain.docstore.document import Document
    from langchain.callbacks import get_openai_callback
    import requests
    from markdownify import markdownify
    from dotenv import load_dotenv
    load_dotenv()
    _txt = []
    for _link in _weblink:
        print(_link)
        _r = requests.get(_link)
        _t1 = markdownify(_r.text, heading_style="ATX")
        _t2 = re.sub(r'\n\s*\n', '\n\n', _t1)
        _t3 = _t2.split("\nTable of contents\n\n")
        _t4 = _t3[-1]
        _t5 = _t4.split("\n## Additional resources\n\n")
        _t6 = _t5[0]
        _t7 = _t6.split("\nTheme\n\n")
        _t8 = _t7[0]
        # print(_t8)
        _txt.append(_t8)
    _weblink_txt = "\n\n".join(_txt)
    with get_openai_callback() as cb:
        llm = ChatOpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0) # gpt-4
        # llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k-0613", temperature=0)
        # llm = OpenAI(temperature=0)
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        texts = text_splitter.split_text(_weblink_txt)
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]).as_retriever()
        docs = docsearch.get_relevant_documents(_q)
        chain = load_qa_chain(llm, chain_type="refine") # stuff/refine
        _re = chain({"input_documents": docs, "question": _q}, return_only_outputs=True)
        _ans = _re["output_text"]
        _ans = _ans.replace("\n\n", "\n")
        _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
        _step = f"{_token_cost}\n\n" + f">>> {_q}\n" + f"<<<\n{_ans}"
    return _ans, _step
# _service = "azure sql managed instance"
# _q = f"Which performance counters can I use to monitor the cost drivers of {_service} and identify a more cost-effective resource that meets the required performance and usage? List the results with brief explanations in numbered format, excluding any additional content.
# # _weblink = [
# #     "https://azure.microsoft.com/en-us/pricing/details/managed-disks"
# #     ]
# _weblink = [
#       "https://azure.microsoft.com/en-us/pricing/details/azure-sql-managed-instance/single/",
#       "https://azure.microsoft.com/en-us/pricing/details/azure-sql-managed-instance/pools/"
#     ]
# _ans, _step = qa_weblink(_q, _weblink)
# print(_q)
# print(_ans)
# print(_step)
# exit()


def qa_weblink_and_parse_to_item(_q, _dj, _service):
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _module_path = _pwd.parent.parent
    sys.path.append(str(_module_path))
    from module.query_vdb import qa_faiss_multi_query
    from dotenv import load_dotenv
    load_dotenv()
    _weblink = _dj[_service]['pricing']
    _ans, _step = qa_weblink(_q, _weblink)
    _ans = _ans.replace("\n\n", "\n")
    print(_ans)
    _item = parse_to_item(_ans)
    _item_log = f"\n----------\n{_q}\n\n{_ans}\n\n{_item}\n----------\n"
    print(_item_log)
    return _item, _item_log


def qa_vdb_and_parse_to_item(_q, _dj, _service):
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _module_path = _pwd.parent.parent
    sys.path.append(str(_module_path))
    from module.query_vdb import qa_faiss_multi_query
    from dotenv import load_dotenv
    load_dotenv()
    _vdb = _dj[_service]['vdb']
    _ans, _step = qa_faiss_multi_query(_q, _vdb)
    _ans = _ans.replace("\n\n", "\n")
    print(_ans)
    _item = parse_to_item(_ans)
    _item_log = f"\n----------\n{_q}\n\n{_ans}\n\n{_item}\n----------\n"
    print(_item_log)
    return _item, _item_log


def list_performance_counters(_dj, _service):
    _list = []
    _log = ""
    _q0 = f"Which performance counters can I use to monitor the cost drivers of {_service} and identify a more cost-effective resource that meets the required performance and usage? List the results with brief explanations in numbered format, excluding any additional content."
    _list.append(_q0)
    _n = 0
    while True:
        _n += 1
        _item, _item_log = qa_weblink_and_parse_to_item(_q0, _dj, _service)
        if _item:
            for i in _item:
                _qi = f"What is the '{i}' of {_service}?"
                _list.append(_qi)
            _log = _item_log
            break
        if _n > 3:
            break
    return _list, _log


def what_topic_and_stepbystep_explanation(_topic, _dj, _service):
    _list = []
    _log = ""
    _q0 = f"What are {_topic} of the {_service}? List the results with brief explanations in numbered format, excluding any additional content."
    _list.append(_q0)
    _n = 0
    _nn = 0
    while True:
        _n += 1
        _item, _item_log = qa_vdb_and_parse_to_item(_q0, _dj, _service)
        if _item:
            for i in _item:
                _qi = ""
                if _topic in ["performance metrics"]:
                    _qi = f"Can you provide a step-by-step explanation of how the '{i}' affect the cost of {_service}?"
                elif _topic in ["pricing options"]:
                    _qi = f"What are the best practices for choosing suitable '{i}' based on usage to save cost?"
                elif _topic in ["cost drivers"]:
                    _qi = f"What are the best practices for choosing suitable '{i}' based on usage to save cost?"
                else:
                    _qi = f"What are the best practices for choosing suitable '{i}' based on usage to save cost?"
                if _qi:
                    _list.append(_qi)
                else:
                    print(f"ERROR: wrong topic: {_topic}")
            _log = _item_log
            break
        if _n > 3:
            _nn += 1
            _item, _item_log = qa_weblink_and_parse_to_item(_q0, _dj, _service)
            if _item:
                for i in _item:
                    _qi = ""
                    if _topic in ["performance metrics"]:
                        _qi = f"Can you provide a step-by-step explanation of how the '{i}' affect the cost of {_service}?"
                    elif _topic in ["pricing options"]:
                        _qi = f"What are the best practices for choosing suitable '{i}' based on usage to save cost?"
                    elif _topic in ["cost drivers"]:
                        _qi = f"What are the best practices for choosing suitable '{i}' based on usage to save cost?"
                    else:
                        _qi = f"What are the best practices for choosing suitable '{i}' based on usage to save cost?"
                    if _qi:
                        _list.append(_qi)
                    else:
                        print(f"ERROR: wrong topic: {_topic}")
                _log = _item_log
                break
        if _nn > 3:
            break
    return _list, _log


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
            # print(_g[i], _g[j])
            _gi = f"'{_g[i]}' in {_c2}"
            _gj = f"'{_g[j]}' in {_c2}"
            j_q0 = f"What's the difference between {_gi} and {_gj}?"
            j_q1 = f"When should I choose {_gi} over {_gj}?"
            j_q2 = f"When should I choose {_gj} over {_gi}?"
            _list.extend([j_q0, j_q1, j_q2])
    # print(_list)
    return _list


def qlist_from_json(_json, _dir, _service):
    import json
    with open(_json, 'r', encoding='utf-8') as jf:
        _dj = json.loads(jf.read())
    _d = _dj[_service]['qlist']
    # print(_d)
    _list = []
    _log = []
    _q_lpc, _q_lpc_log = list_performance_counters(_dj, _service)
    _list.extend(_q_lpc)
    _log.append(_q_lpc_log)
    for i in _d.keys():
        i_list, i_list_log = what_topic_and_stepbystep_explanation(i, _dj, _service)
        _log.append(i_list_log)
        _list.extend(i_list)
        if 'key_concept' in _d[i]:
            _d_kc = _d[i]['key_concept']
            for j in _d_kc.keys():
                # print(i, j)
                if _d_kc[j]:
                    # print(j)
                    _compare_list = comparison_between_itmes(i, j, _dj, _service)
                    _list.extend(_compare_list)
                else:
                    # print(j)
                    _qj = f"Can you provide a step-by-step explanation of how the {j} affect the cost of {_service}?"
                    _list.extend([_qj])
        # else:
        #     print(i)
    _qlist = sorted(list(set(_list)))
    # _qlist = list(set(_list))
    _qlist_str = "\n".join(_qlist)
    writeF(_dir, '_qlist', _qlist_str)
    _log_str = "\n".join(_log)
    writeF(_dir, '_qlist_log', _log_str)
    return _qlist


def get_ans_from_qlist(_json, _dir, _service):
    import json
    with open(_json, 'r', encoding='utf-8') as jf:
        _dj = json.loads(jf.read())
    _qlist = readF(_dir, "_qlist").split("\n")
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _pa_path = _pwd.parent.parent
    sys.path.append(str(_pa_path))
    from module.query_vdb import qa_faiss_multi_query
    from dotenv import load_dotenv
    load_dotenv()
    import os, time
    _vdb = _dj[_service]['vdb']
    _ans = []
    a, b, c= 0, 0, 0
    for i in _qlist:
        a +=1
        _fn = i.split("?")
        _fn0 = _fn[0].replace("/", "|")
        _fn_ans = "_ans_"+_fn0
        _fn_step = "_step_"+_fn0
        #####
        _ans_f = os.path.join(_dir, "_ans_", _fn_ans)
        _step_f = os.path.join(_dir, "_step_", _fn_ans)
        if not os.path.exists(_ans_f):
            b += 1
            _q = f"{i} Please output in concise English."
            print(_q)
            i_ans, i_step = "", ""
            i_ans, i_step = qa_faiss_multi_query(_q, _vdb)
            writeF(os.path.join(_dir, "_ans_"), _fn_ans, i_ans)
            writeF(os.path.join(_dir, "_step_"), _fn_step, i_step)
            # time.sleep(4)
            _ans.append(i_ans)
        else:
            c +=1
            i_ans = readF(os.path.join(_dir, "_ans_"), _fn_ans)
            i_step = readF(os.path.join(_dir, "_step_"), _fn_step)
            _ans.append(i_ans)
    print(f"total({a}) = new({b}) + old({c})")
    _ans_str = ""
    for i in range(len(_qlist)):
        _ans_str += f"## {_qlist[i]}\n\n" + f"{_ans[i]}\n\n"
    writeF(_dir, '_ans', _ans_str)


def _chat_with_sys_human(_info, _service, _sys, _human):
    import os
    from dotenv import load_dotenv
    load_dotenv()
    from langchain.callbacks import get_openai_callback
    from langchain.chat_models import ChatOpenAI
    from langchain import LLMChain
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )
    from langchain.prompts import load_prompt
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _prompt_path = os.path.join(_pwd.parent.parent, 'prompt')
    sys_file = os.path.join(_prompt_path, _sys)
    human_file = os.path.join(_prompt_path, _human)
    system_message_prompt = SystemMessagePromptTemplate.from_template_file(
        sys_file,
        input_variables=[]
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template_file(
        human_file,
        input_variables=["info", "service"]
    )
    rule_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    with get_openai_callback() as cb:
        # llm = ChatOpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0)
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k-0613", temperature=0)
        chain = LLMChain(llm=llm, prompt=rule_prompt)
        _re = chain.run(info=_info, service=_service)
        _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
        _rule = _re.strip().split("\n")
        _rule_step = f"{_token_cost}\n\n" + "="*20+" prompt "+"="*20+"\n" + rule_prompt.format(info=_info, service=_service) + "="*20+" prompt "+"="*20+"\n" + f"extracted rules:\n\n" + "\n".join(_rule)
    return _rule, _rule_step


def _uniq(_rule):
    _rule_ = {}
    import re
    for i in _rule:
        i = i.strip()
        if re.match('^\d+\.', i):
            if not re.match('.*\:$', i):
                i_str = re.sub('^\d+\. ', '', i)
                # print(f"'{i_str}'")
                _rule_[i_str] = 1
    return _rule_
# _rule=["1. The 'Business Critical' service tier has the following limitations: ", "2. Slower geo-recovery time.", "3. A: B"]
# print(_uniq(_rule))
# exit()


def _similarity(_s1, _s2, _model):
    # from sentence_transformers import SentenceTransformer
    # model = SentenceTransformer('all-MiniLM-L12-v2')
    from scipy.spatial.distance import cosine
    _s1_embedding = _model.encode(_s1)
    _s2_embedding = _model.encode(_s2)
    _cosine = 1 - cosine(_s1_embedding, _s2_embedding)
    _score = _cosine
    return _score


##### 相似的string中，取最后一个
# abc abc abc
# abc abc abc
# abc abc abc
# abc abc abc1
##### 取'abc abc abc1'
def _clean(_rm, _model):
    _rc = []
    for i in range(len(_rm)):
        _n = 0
        for j in range(i+1, len(_rm)):
            if _n == 0:
                _rmi = _rm[i].strip()
                _rmj = _rm[j].strip()
                if _rmi in _rmj or _rmj in _rmi:
                    _n = 1
                else:
                    _s = _similarity(_rmi, _rmj, _model)
                    # print(f"{_rmi}\n{_rmj}\n{_s}\n\n")
                    if _s > 0.98:
                        _n = 1
        if _n == 0:
            _rc.append(_rm[i])
    return _rc


def _rule(_ans_str, _dir, _service):
    _sys = 'azure_rule_sys.txt'
    _human = 'azure_rule_human_0.txt'
    _info = _ans_str
    _rule1, _rule1_step = _chat_with_sys_human(_info, _service, _sys, _human)
    print(len(_rule1))
    _rule2, _rule2_step = _chat_with_sys_human(_info, _service, _sys, _human)
    print(len(_rule2))
    _rule3, _rule3_step = _chat_with_sys_human(_info, _service, _sys, _human)
    print(len(_rule3))
    _rule1_ = _uniq(_rule1)
    _rule2_ = _uniq(_rule2)
    _rule3_ = _uniq(_rule3)
    print('uniq done!', len(_rule1_), len(_rule2_), len(_rule3_))
    _rule_ = {}
    _rule_ = _rule1_ | _rule2_
    _rule_ |= _rule3_
    _rm = list(_rule_.keys())
    print('merge done!', len(_rm))
    from sentence_transformers import SentenceTransformer
    _model = SentenceTransformer('all-MiniLM-L12-v2')
    _rc = _clean(_rm, _model)
    print('clean done!', len(_rc))
    print(len(_rule1), len(_rule2), len(_rule3), '->', len(_rule1_), len(_rule2_), len(_rule3_), '->' , len(_rm), '->' , len(_rc))
    _rule_str = ""
    _n = 0
    for i in sorted(_rc):
        _n += 1
        # _rule_str += f"{_n}. {i}\n"
        _rule_str += f"{i}\n"
    _rule_step = [_rule1_step, _rule2_step, _rule3_step]
    _out_rule = '_rule'
    _out_rule_step = '_rule_step'
    writeF(_dir, _out_rule, _rule_str)
    writeF(_dir, _out_rule_step, "\n\n".join(_rule_step))


def extract_rule(_dir, _service):
    import os
    _ans_f = os.path.join(_dir, '_ans')
    with open(_ans_f, 'r', encoding='utf-8') as rf:
        _ans_str = rf.read()
    _rule(_ans_str, _dir, _service)


def _rulebook(_ans_str, _dir, _service):
    _sys = 'azure_rulebook_sys.txt'
    _human = 'azure_rulebook_human_0.txt'
    _info = _ans_str
    _rulebook, _rulebook_step = _chat_with_sys_human(_info, _service, _sys, _human)
    _out_rule = '_rulebook'
    _out_rule_step = '_rulebook_step'
    writeF(_dir, _out_rule, _rulebook)
    writeF(_dir, _out_rule_step, _rulebook_step)


def extract_rulebook(_ans_f, _dir, _service):
    import os
    _ans_f = os.path.join(_dir, '_ans')
    with open(_ans_f, 'r', encoding='utf-8') as rf:
        _ans_str = rf.read()
    _rulebook(_ans_str, _dir, _service)

