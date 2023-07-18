import sys
from pathlib import Path
from pprint import pprint
_pwd = Path(__file__).absolute()
_pa_path = _pwd.parent.parent
# print(_pa_path)
sys.path.append(str(_pa_path))
# pprint(sys.path)
from module.query_vdb import qa_faiss_multi_query_azure
from dotenv import load_dotenv
load_dotenv()

##### generate dir
import os
from module.util import timestamp_now
_ts = f"./tmp_{str(timestamp_now())}/"
if not os.path.exists(_ts):
    os.makedirs(_ts)

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

##### 1) get No. of disk types
_q1 = "how many managed disk typs in Azure?"
_ans1, _step1 = qa_faiss_multi_query_azure(_q1)
writeF(_ts, '_ans1', _ans1)
writeF(_ts, '_step1', _step1)

##### 2) generate question list
from langchain.callbacks import get_openai_callback
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain import LLMChain
qlist_template = \
"""
If there are two types of A/B/C, you should generate the question list as below:
--------------------
what's A?
what's the unique feature of A?
waht's the limitation of A?
when to choose A?
what's B?
what's the unique feature of B?
waht's the limitation of B?
when to choose B?
what's C?
what's the unique feature of C?
waht's the limitation of C?
when to choose C?
what's the difference between A and B?
when to choose A over B?
when to choose B over A?
what's the difference between A and C?
when to choose A over C?
when to choose C over A?
what's the difference between B and C?
when to choose B over C?
when to choose C over B?
--------------------
Giving the following information:
{info}
What question list you should generated? Remember output the questions only, nothing else.
"""
_info = readF(_ts, '_ans1')
qlist_prompt = PromptTemplate.from_template(qlist_template)
with get_openai_callback() as cb:
    llm = ChatOpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0)
    chain = LLMChain(llm=llm, prompt=qlist_prompt)
    _re = chain.run(info=_info)
    _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
    _ans2 = _re.strip()
    _step2 = f"{_token_cost}\n\n" + "="*20+" prompt "+"="*20+"\n" + qlist_prompt.format(info=_ans1)
writeF(_ts, '_ans2', _ans2)
writeF(_ts, '_step2', _step2)

##### 3) get all ans from question list
import time
_qlist = readF(_ts, '_ans2').split("\n")
# print(_qlist)
_ans3 = []
for i in _qlist:
    i_ans, i_step = qa_faiss_multi_query_azure(i)
    writeF(_ts, '_ans3_'+i.replace("?", ""), i_ans)
    writeF(_ts, '_step3_'+i.replace("?", ""), i_step)
    time.sleep(5)
    _ans3.append(i_ans)

_ans3_str = ""
for i in range(len(_qlist)):
    _ans3_str += f"## {_qlist[i]}\n\n" + f"{_ans3[i]}\n\n"
writeF(_ts, '_ans3', _ans3_str)

