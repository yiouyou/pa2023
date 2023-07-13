def llm_azure_rules(_text):
    _ans, _steps = "", ""
    from langchain.callbacks import get_openai_callback
    from dotenv import load_dotenv
    load_dotenv()
    from langchain.prompts.pipeline import PipelinePromptTemplate
    from langchain.prompts.prompt import PromptTemplate
    from langchain.llms import OpenAI
    from langchain import LLMChain
    full_template = """{introduction}

{info}

{example}

{start}"""
    full_prompt = PromptTemplate.from_template(full_template)

    introduction_template = """You are now a cloud cost optimization expert. I want you to build a catalog of rules to define the rules of what you can and cannot do when optimizing managed disks on azure, i.e. converting from one disk type to another, and resizing existing disk types. Every time you receive new information, you should find out if there are any new rules or restrictions, present them with a short number."""
    introduction_prompt = PromptTemplate.from_template(introduction_template)

    info_template = """The following is the given information from which the rule needs to be extracted:
------------------------------information
{given_info}
------------------------------"""
    info_prompt = PromptTemplate.from_template(info_template)

    example_template = """The following is an example list of extracted rules:
------------------------------example list
#, Rule, Rule Area
1, You can convert a managed disk from one type to another (e.g., from Standard HDD to Premium SSD or vice versa, Right-Typing
2, The performance of a managed disk (IOPS and throughput) is directly related to its size, thus the convertion must respect the monitored need for IOPS and Throughput of the target disk, when converting type, Right-Typing
3, Convertion betwen Standard HDD, Standard SSD and Premium SSD can be done by shutting down the VM and executing the conversion, while conversion to and from Premium SSD v2 and Ultra requires extensive downtime, Right-Typing
4, Only Premium SSD, Standard SSD and Standard HDD can be used for Operating systems disks, All types of disks can be used for data disks, Right-Typing
5, Not all disk types are available in all Azure regions. Therefore, the availability of certain disk types for conversion  depends on the region., Right-Typing
6, Only select Virtual Machines supports premium storage like Ultra Disk and Premium SSD v2. If VMType=XXXX Prem. Supported then else if, Right-Typing
7, The target disk must meet the redundancy requirements of the source disk. Ie. LRS to LRS or ZRS to ZRS, Right-Typing
8, Only Standard SSD and Premium SSD supports ZRS, Right-Typing
------------------------------"""
    example_prompt = PromptTemplate.from_template(example_template)

    start_template = """Now, please generate the rules based on provided information and examples:"""
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
        llm = OpenAI(temperature=0.1)
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
    # chat = ChatOpenAI(temperature=0)
    # _re = chat([HumanMessage(content="Translate this sentence from English to Chinese: I love programming.")])
    # _ans = _re.content

    with get_openai_callback() as cb:
        chat = ChatOpenAI(temperature=0)
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

