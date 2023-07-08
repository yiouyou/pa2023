def agent_react_docstore_wiki(_ask):
    from langchain import OpenAI
    from langchain.agents import AgentType
    from langchain.agents import initialize_agent
    from langchain.callbacks import get_openai_callback
    from module.tools import tools_react_docstore_wiki
    from module.util import parse_intermediate_steps
    max_execution_time=25
    llm_openai = OpenAI(temperature=0)
    _react_docstore = initialize_agent(tools_react_docstore_wiki, llm_openai, agent=AgentType.REACT_DOCSTORE, verbose=True, return_intermediate_steps=True, max_execution_time=max_execution_time, early_stopping_method="generate")
    _ans, _steps = "", ""
    with get_openai_callback() as cb:
        _re = _react_docstore(_ask)
        # print(_re)
        _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
        print(_token_cost)
        _ans = _re["output"]
        _steps = f"{_token_cost}\n\n" + parse_intermediate_steps(_re["intermediate_steps"])
    return [_ans, _steps]


def agent_self_ask_with_search(_ask):
    from langchain import OpenAI
    from langchain.agents import AgentType
    from langchain.agents import initialize_agent
    from langchain.callbacks import get_openai_callback
    from module.tools import tools_self_ask_with_search
    from module.util import parse_intermediate_steps
    max_execution_time=25
    llm_openai = OpenAI(temperature=0)
    _self_ask_with_search = initialize_agent(tools_self_ask_with_search, llm_openai, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True, return_intermediate_steps=True, max_execution_time=max_execution_time, early_stopping_method="generate")
    _ans, _steps = "", ""
    with get_openai_callback() as cb:
        _re = _self_ask_with_search(_ask)
        # print(_re)
        _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
        print(_token_cost)
        _ans = _re["output"]
        _steps = f"{_token_cost}\n\n" + parse_intermediate_steps(_re["intermediate_steps"])
    return [_ans, _steps]


def agent_zeroshot(_ask, _tools):
    from langchain import OpenAI, LLMChain
    from langchain.agents import ZeroShotAgent, AgentExecutor
    from langchain.callbacks import get_openai_callback
    prefix = """Answer the following questions as best you can. You have access to the following tools:"""
    suffix = """When answering, you MUST speak in the following language: {language}."

Question: {input}
{agent_scratchpad}"""
    prompt = ZeroShotAgent.create_prompt(
        _tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "language", "agent_scratchpad"]
    )
    llm_chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=prompt
    )
    agent = ZeroShotAgent(
        llm_chain=llm_chain,
        tools=_tools
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=_tools,
        verbose=True
    )
    _ans, _steps = "", ""
    with get_openai_callback() as cb:
        _ans = agent_executor.run(
            input=_ask,
            language="Chinese"
        )
        _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
        print(_token_cost)
        _steps = f"{_token_cost}\n\n" + prompt.template + "\n\n"
    return [_ans, _steps]


def agent_zeroshot_google(_ask):
    from module.tools import tools_zeroshot_google
    [_ans, _steps] = agent_zeroshot(_ask, tools_zeroshot_google)
    return [_ans, _steps]


def agent_zeroshot_azure_langchain_googleserp(_ask):
    from module.tools import tools_faiss_azure_langchain_googleserp
    [_ans, _steps] = agent_zeroshot(_ask, tools_faiss_azure_langchain_googleserp)
    return [_ans, _steps]


if __name__ == "__main__":

    import sys
    from pathlib import Path
    from pprint import pprint
    # pprint(sys.path)
    _pwd = Path(__file__).absolute()
    _pa_path = _pwd.parent.parent.parent
    # print(_pa_path)
    sys.path.append(str(_pa_path))
    # pprint(sys.path)
    from dotenv import load_dotenv
    load_dotenv()
    
    # _re = agent_react_docstore_wiki("Author David Chanoff has collaborated with a U.S. Navy admiral who served as the ambassador to the United Kingdom under which President?")
    # print(_re)

    # _re = agent_self_ask_with_search("What is the hometown of the reigning men's U.S. Open champion?")
    # print(_re)

    # _re = agent_zeroshot_google("How many people live in canada as of 2023?")
    # print(_re)

    _re = agent_zeroshot_azure_langchain_googleserp("How many people live in canada as of 2023?")
    print(_re)
