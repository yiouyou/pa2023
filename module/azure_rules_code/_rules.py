def llm_azure_rules(_text):
    _ans, _steps = "", ""
    from langchain.callbacks import get_openai_callback
    from dotenv import load_dotenv
    load_dotenv()
    from langchain.prompts.pipeline import PipelinePromptTemplate
    from langchain.prompts.prompt import PromptTemplate
    from langchain.llms import OpenAI
    from langchain import LLMChain
    import os
    full_template = """{introduction}

{info}

{example}

{start}"""
    full_prompt = PromptTemplate.from_template(full_template)

    introduction_template = """You are now a cloud cost optimization expert. I want you to build a catalog of rules to define the rules of what you can and cannot do when optimizing managed disks on azure, i.e. converting from one disk type to another, and resizing existing disk types. Every time you receive new information, you should find out if there are any new rules or restrictions, present them with a short number."""
    introduction_prompt = PromptTemplate.from_template(introduction_template)

    info_template = """The following is the given information from which the rule needs to be extracted:
------------------------------
{given_info}
------------------------------"""
    info_prompt = PromptTemplate.from_template(info_template)

    example_template = """output in the following format:
------------------------------
No, Rule
1, blabla
2, blabla
...
------------------------------"""
    example_prompt = PromptTemplate.from_template(example_template)

    start_template = """Now, please generate the rules based on provided information only, nothing else:"""
    start_prompt = PromptTemplate.from_template(start_template)

    input_prompts = [
        ("introduction", introduction_prompt),
        ("info", info_prompt),
        ("example", example_prompt),
        ("start", start_prompt)
    ]
    pipeline_prompt = PipelinePromptTemplate(final_prompt=full_prompt, pipeline_prompts=input_prompts)
    # print(pipeline_prompt.input_variables)
    with get_openai_callback() as cb:
        llm = OpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0.1)
        chain = LLMChain(llm=llm, prompt=pipeline_prompt)
        _re = chain.run(
            given_info=_text,
        )
        _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
        print(_token_cost)
        _ans = _re.strip()
        _steps = f"{_token_cost}\n\n" + "="*20+" prompt "+"="*20+"\n" + pipeline_prompt.format(given_info=_text)

    return [_ans, _steps]


def chat_azure_rules(_text):
    _ans, _steps = "", ""
    from langchain.callbacks import get_openai_callback
    from dotenv import load_dotenv
    load_dotenv()
    from langchain.prompts import (
        ChatPromptTemplate,
        PromptTemplate,
        SystemMessagePromptTemplate,
        AIMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )
    from langchain.schema import (
        AIMessage,
        HumanMessage,
        SystemMessage
    )
    from langchain.chat_models import ChatOpenAI
    from langchain import LLMChain
    import os
    sys_template="""
You are a helpful assistant that translates {input_language} to {output_language}.
"""
    sys_msg_prompt = SystemMessagePromptTemplate.from_template(sys_template)

    human_template="""
{text}
"""
    human_msg_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [sys_msg_prompt,
         human_msg_prompt]
    )

    # _ChatPromptValue = chat_prompt.format_prompt(
    #     input_language="English",
    #     output_language="Chinese",
    #     text=_text
    # )
    # print(_ChatPromptValue)
    # _messages = _ChatPromptValue.to_messages()
    # print(_messages)
    # chat = ChatOpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0)
    # _re = chat([HumanMessage(content="Translate this sentence from English to Chinese: I love programming.")])
    # _ans = _re.content

    with get_openai_callback() as cb:
        chat = ChatOpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0)
        chain = LLMChain(llm=chat, prompt=chat_prompt)
        _re = chain.run(
            input_language="English",
            output_language="French",
            text="I love programming."
        )
        _token_cost = f"Tokens: {cb.total_tokens} = (Prompt {cb.prompt_tokens} + Completion {cb.completion_tokens}) Cost: ${format(cb.total_cost, '.5f')}"
        print(_token_cost)
        _ans = _re
        _steps = f"{_token_cost}\n\n"

    return [_ans, _steps]


if __name__ == "__main__":

    _text = """
"""
    _re1 = llm_azure_rules(_text)
    print(_re1)

    _re2 = chat_azure_rules(_text)
    print(_re2)

