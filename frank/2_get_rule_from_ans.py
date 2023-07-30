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
        if re.match('^\d+\.', i):
            i_str = re.sub('^\d+\. ', '', i)
            # print(f"'{i_str}'")
            _rule_[i_str] = 1
    return _rule_

def _similarity(_s1, _s2):
    from sentence_transformers import SentenceTransformer
    from scipy.spatial.distance import cosine
    model = SentenceTransformer('all-MiniLM-L12-v2')
    _s1_embedding = model.encode(_s1)
    _s2_embedding = model.encode(_s2)
    _cosine = 1 - cosine(_s1_embedding, _s2_embedding)
    _score = _cosine
    return _score


##### 相似的string中，取最后一个
# abc abc abc
# abc abc abc
# abc abc abc
# abc abc abc1
##### 取'abc abc abc1'
def _clean(_rk):
    _rc = []
    for i in range(len(_rk)):
        _n = 0
        for j in range(i+1, len(_rk)):
            if _n == 0:
                _rki = _rk[i].strip()
                _rkj = _rk[j].strip()
                if _rki in _rkj or _rkj in _rki:
                    _n = 1
                else:
                    _s = _similarity(_rki, _rkj)
                    # print(f"{_rki}\n{_rkj}\n{_s}\n\n")
                    if _s > 0.98:
                        _n = 1
        if _n == 0:
            _rc.append(_rk[i])
    return _rc


def _rule(_ans_str, _dir, _service):
    _sys = 'azure_rule_sys.txt'
    _human = 'azure_rule_human_0.txt'
    _info = _ans_str
    _out_rule = '_rule'
    _out_rule_step = '_rule_step'
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
    _rk = list(_rule_.keys())
    print('merge done!', len(_rk))
    _rc = _clean(_rk)
    print('clean done!', len(_rc))
    _rule_str = ""
    _n = 0
    for i in sorted(_rc):
        _n += 1
        # _rule_str += f"{_n}. {i}\n"
        _rule_str += f"{i}\n"
    print(len(_rule1), len(_rule2), len(_rule3), '->' , len(_rk), '->' , len(_rc))
    writeF(_dir, _out_rule, _rule_str)
    _rule_step = [_rule1_step, _rule2_step, _rule3_step]
    writeF(_dir, _out_rule_step, "\n\n".join(_rule_step))


def extract_rules(_ans_f, _dir, _service):
    with open(_ans_f, 'r', encoding='utf-8') as rf:
        _ans_str = rf.read()
    _rule(_ans_str, _dir, _service)



if __name__ == "__main__":

    import os, sys

    ##### get rules
    _dir = sys.argv[1]
    _service = sys.argv[2]
    _ans_f = os.path.join(_dir, '_ans')
    extract_rules(_ans_f, _dir, _service)
    # python 2_get_rule_from_ans.py tmp_azure_managed_disk_1690529169 "azure managed disk"
    # python 2_get_rule_from_ans.py tmp_azure_sql_database_1690531985 "azure sql database"
    # python 2_get_rule_from_ans.py tmp_azure_sql_managed_instance_1690535170 "azure sql managed instance"
    # python 2_get_rule_from_ans.py tmp_azure_static_web_apps_1690531612 "azure static web apps"

    # with open('tmp_azure_managed_disk_1690529169/_rule', 'r') as rf:
    #     _f = rf.readlines()
    # print(len(_f))
    # _cf = _clean(_f)
    # print(len(_cf))
    # for i in _cf:
    #     print(i)
