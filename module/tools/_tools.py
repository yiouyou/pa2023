from langchain.utilities import GoogleSerperAPIWrapper
search_google_serp = GoogleSerperAPIWrapper()

from langchain import SerpAPIWrapper
search_serp = SerpAPIWrapper()

from langchain.utilities import GoogleSearchAPIWrapper
search_goolge = GoogleSearchAPIWrapper()

from langchain import Wikipedia
from langchain.agents.react.base import DocstoreExplorer
docstore_wiki = DocstoreExplorer(Wikipedia())



from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import os
llm = ChatOpenAI(model_name=os.getenv('OPENAI_MODEL'), temperature=0)

from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from module.query_vdb import get_faiss_vdb_retriever, get_faiss_multi_query_retriever
from pathlib import Path
_pwd = Path(__file__).absolute()
_vdb_path = _pwd.parent.parent.parent

_azure = str(_vdb_path / "vdb" / "azure_virtual_machines_plus")
# _retriever_azure = get_faiss_vdb_retriever(_azure)
_retriever_azure = get_faiss_multi_query_retriever(_azure)
retriev_azure = RetrievalQA.from_chain_type(llm, retriever=_retriever_azure)

_langchain = str(_vdb_path / "vdb" / "langchain_python_documents")
# _retriever_langchain = get_faiss_vdb_retriever(_langchain)
_retriever_langchain = get_faiss_multi_query_retriever(_langchain)
retriev_langchain = RetrievalQA.from_chain_type(llm, retriever=_retriever_langchain)
