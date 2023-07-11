##### search
from langchain.utilities import GoogleSerperAPIWrapper
search_google_serp = GoogleSerperAPIWrapper()

from langchain import SerpAPIWrapper
search_serp = SerpAPIWrapper()

from langchain.utilities import GoogleSearchAPIWrapper
search_goolge = GoogleSearchAPIWrapper()

from langchain import Wikipedia
from langchain.agents.react.base import DocstoreExplorer
docstore_wiki = DocstoreExplorer(Wikipedia())


##### llm related
from dotenv import load_dotenv
load_dotenv()

from langchain.llms import OpenAI
from langchain import LLMMathChain
llm_math_chain = LLMMathChain.from_llm(
    llm=OpenAI(temperature=0),
    verbose=True
)

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from module.query_vdb import get_faiss_multi_query_retriever, get_faiss_vdb_retriever
from pathlib import Path
_pwd = Path(__file__).absolute()
_vdb_path = _pwd.parent.parent.parent

### faiss_azure
_azure = str(_vdb_path / "vdb" / "azure_virtual_machines_plus")
# _retriever_azure = get_faiss_vdb_retriever(_azure)
_retriever_azure = get_faiss_multi_query_retriever(_azure)
retriev_azure = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    retriever=_retriever_azure
)

### faiss_langchain
_langchain = str(_vdb_path / "vdb" / "langchain_python_documents")
# _retriever_langchain = get_faiss_vdb_retriever(_langchain)
_retriever_langchain = get_faiss_multi_query_retriever(_langchain)
retriev_langchain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    retriever=_retriever_langchain
)
