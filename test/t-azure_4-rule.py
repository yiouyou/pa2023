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

##### 4) extract rules
from langchain.callbacks import get_openai_callback
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.chat_models import JinaChat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
# _dir = 'tmp_disk_1689564655'
# _dir = 'tmp_disk_1689855176'
# _dir = 'tmp_sql_1689849358'
_dir = 'tmp_webapps_1689850394'
_info = readF(_dir, '_ans3')
_service = 'static web apps' # 'managed disk', 'SQL database', 'SQL managed instance', 'static web apps'
_out_ans = '_ans40'
_out_step = '_step40'
# print(_info)
sys_template = (
    "You are a cost optimization expert, providing cost optimization suggestions for Azure cloud service customers. In order to achieve this goal, it is necessary to first construct a list of cost optimization rules, listing what can and cannot be done in various situations; then write python code according to the cost optimization rules, which is related to inputting the usage status of customer cloud services When using data, all feasible optimization measures can be directly calculated and recommended with priority of cost and safety."
)
system_message_prompt = SystemMessagePromptTemplate.from_template(sys_template)
human_template = \
"""
Giving the following information:
--------------------
{info}
--------------------
What are necessary non-duplicative rules that you can extract to optimize the usage of Azure {service}?""" + \
""" In order to make the cost optimization step easier to execute, each rule should not be too complicated, usually the simpler the rule, the easier it is to be executed, the better. For each rule, output it as the format '#. rule_content' in which '#' is number of index, 'rule_content' is the rule it self. Please extract as many effective and non-repeated rules as possible:
"""
# """ Remember to cover as many details as possible, the simpler each rule the better. Output only non-duplicative rules with numeric indices in the format '1. rule_content', nothing else:
# """


human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
rule_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)
import os, re
with get_openai_callback() as cb:
    llm = ChatOpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0)
    chain = LLMChain(llm=llm, prompt=rule_prompt)
    _re = chain.run(info=_info, service=_service)
    _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
    _ans4 = _re.strip().split("\n")
    _step4 = f"{_token_cost}\n\n" + "="*20+" prompt "+"="*20+"\n" + rule_prompt.format(info=_info, service=_service) + "="*20+" prompt "+"="*20+"\n" + f"extracted rules:\n\n" + "\n".join(_ans4)
    # print(_step4)
    # print(_ans4)
if " - " in _re:
    _ans4_ = []
    for i in _ans4:
        if re.match('^\d+\.', i):
            i_str = re.sub('^\d+\. ', '', i)
            # print(f"'{i_str}'")
            _ans4_.append(i_str)
        if re.match('^\s+\- ', i):
            i_str = re.sub('^\s+\- ', '- ', i)
            # print(f"'{i_str}'")
            _ans4_.append(i_str)
    writeF(_dir, _out_ans, "\n".join(_ans4_))
else:
    _ans4_ = {}
    for i in _ans4:
        if re.match('^\d+\.', i):
            i_str = re.sub('^\d+\. ', '', i)
            # print(f"'{i_str}'")
            _ans4_[i_str] = 1
    writeF(_dir, _out_ans, "\n".join(sorted(_ans4_.keys())))

print(len(_ans4))
print(len(_ans4_))
writeF(_dir, _out_step, _step4)
