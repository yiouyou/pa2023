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

##### 5) remove duplicated rules
import os
from langchain.callbacks import get_openai_callback
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain import LLMChain
_dir = 'tmp_1689564655'
# _dir = 'tmp_1689566000'
_info = readF(_dir, '_ans44')

clean_template = \
"""
Giving the following list:
--------------------
{info}
--------------------
Please remove ALL duplicate entries in the list:
"""
clean_prompt = PromptTemplate.from_template(clean_template)
with get_openai_callback() as cb:
    llm = ChatOpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0)
    chain = LLMChain(llm=llm, prompt=clean_prompt)
    _re = chain.run(info=_info)
    _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
    _ans5 = _re.strip()
    _step5 = f"{_token_cost}\n\n" + "="*20+" prompt "+"="*20+"\n" + clean_prompt.format(info=_info)
writeF(_dir, '_ans55', _ans5)
writeF(_dir, '_step55', _step5)

