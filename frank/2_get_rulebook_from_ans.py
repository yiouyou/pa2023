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
        _rulebook = _re.strip()
        _rulebook_step = f"{_token_cost}\n\n" + "="*20+" prompt "+"="*20+"\n" + rule_prompt.format(info=_info, service=_service) + "="*20+" prompt "+"="*20+"\n" + f"extracted rulebook:\n\n" + _re
    return _rulebook, _rulebook_step


def _rulebook(_ans_str, _dir, _service):
    _sys = 'azure_rulebook_sys.txt'
    _human = 'azure_rulebook_human_0.txt'
    _info = _ans_str
    _out_rule = '_rulebook'
    _out_rule_step = '_rulebook_step'
    _rulebook, _rulebook_step = _chat_with_sys_human(_info, _service, _sys, _human)
    writeF(_dir, _out_rule, _rulebook)
    writeF(_dir, _out_rule_step, _rulebook_step)


def extract_rulebook(_ans_f, _dir, _service):
    with open(_ans_f, 'r', encoding='utf-8') as rf:
        _ans_str = rf.read()
    _rulebook(_ans_str, _dir, _service)



if __name__ == "__main__":

    import os, sys

    ##### get rules
    _dir = sys.argv[1]
    _service = sys.argv[2]
    _ans_f = os.path.join(_dir, '_ans')
    extract_rulebook(_ans_f, _dir, _service)
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
