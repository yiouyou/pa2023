from ._faiss import get_faiss_ST, pretty_print_docs

def get_faiss_multi_query_retriever(_db_name):
    from langchain.chat_models import ChatOpenAI
    from langchain.retrievers.multi_query import MultiQueryRetriever
    from typing import List
    from pydantic import BaseModel, Field
    from langchain import LLMChain
    from langchain.prompts import PromptTemplate
    from langchain.output_parsers import PydanticOutputParser

    class LineList(BaseModel):
        # "lines" is the key (attribute name) of the parsed output
        lines: List[str] = Field(description="Lines of text")

    class LineListOutputParser(PydanticOutputParser):
        def __init__(self) -> None:
            super().__init__(pydantic_object=LineList)
        def parse(self, text: str) -> LineList:
            lines = text.strip().split("\n")
            return LineList(lines=lines)
    output_parser = LineListOutputParser()
    
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. 
Provide these alternative questions seperated by newlines.
Original question: {question}""",
    )
    llm = ChatOpenAI(temperature=0)
    llm_chain = LLMChain(llm=llm,prompt=QUERY_PROMPT,output_parser=output_parser)
    _db = get_faiss_ST(_db_name)
    _base_retriever = _db.as_retriever()
    _multi_retriever = MultiQueryRetriever(
        retriever=_base_retriever,
        llm_chain=llm_chain,
        parser_key="lines"
    )
    return _multi_retriever

def qa_faiss_retriever_multi_query(_query, _db_name):
    _ans, _steps = "", ""
    from pprint import pprint
    from langchain.callbacks.manager import (
        AsyncCallbackManagerForRetrieverRun,
        CallbackManagerForRetrieverRun,
    )
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI
    from dotenv import load_dotenv
    load_dotenv()
    import os
    llm = ChatOpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0)
    _retriever = get_faiss_multi_query_retriever(_db_name)
    _run_manager = CallbackManagerForRetrieverRun.get_noop_manager()
    _generated_queries = _retriever.generate_queries(_query, _run_manager)
    pprint(_generated_queries)
    _docs = _retriever.get_relevant_documents(_query)
    _pretty = pretty_print_docs(_docs)
    _qa_chain = RetrievalQA.from_chain_type(llm, retriever=_retriever)
    _ans = _qa_chain.run(_query)
    _steps = "\n".join(_retriever.generate_queries(_query, _run_manager)) + f"\n\n{'-' * 100}\n" + _pretty
    return [_ans, _steps]

def qa_faiss_multi_query(_query, _db):
    _ans, _steps = "", ""
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _faiss_path = _pwd.parent.parent.parent
    _db_name = str(_faiss_path / "vdb" / _db)
    print(f"db_name: {_db_name}")
    _ans, _steps = qa_faiss_retriever_multi_query(_query, _db_name)
    return [_ans, _steps]

def qa_faiss_multi_query_azure(_query):
    _ans, _steps = "", ""
    _ans, _steps = qa_faiss_multi_query(_query, "azure_virtual_machines_plus")
    return [_ans, _steps]

def qa_faiss_multi_query_langchain(_query):
    _ans, _steps = "", ""
    _ans, _steps = qa_faiss_multi_query(_query, "langchain_python_documents")
    return [_ans, _steps]


if __name__ == "__main__":

    from _faiss import get_faiss_ST, pretty_print_docs

    _qa = [
        # "how to save money on disk?",
        # "how many disk types are billed per actually allocated disk size?",
        # "how many disk types are billed per actually allocated disk size and how many is billed in buckets?",
        # "can all disks be used to host operating systems for virtual machines?",
        "how many disk types can be used as OS disk, and what are they and why?",
        # "how many disk types can not be used as OS disk, and what are they and why?",
    ]
    for _q in _qa:
        print(_q)
        _re= qa_faiss_multi_query_azure(_q)
        print(f"\n>>>'{_q}'\n<<<'{_re[0]}'\n")

    # _qa = [
    #     "what's the difference between Agent and Chain in Langchain?"
    # ]
    # for _q in _qa:
    #     print(_q)
    #     _re= qa_faiss_multi_query_langchain(_q)
    #     print(f"\n>>>'{_q}'\n<<<'{_re[0]}'\n")

