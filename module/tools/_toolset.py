from ._tools import search_goolge
from ._tools import search_google_serp
from ._tools import search_serp
from ._tools import docstore_wiki
from ._tools import retriev_azure
from ._tools import retriev_langchain

from langchain.agents import Tool


tools_search_serp = [
    Tool(
        name = "Current Search",
        func=search_serp.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]

tools_zeroshot_google = [
    Tool(
        name="Search",
        func=search_goolge.run,
        description="useful for when you need to answer questions about current events",
    )
]

tools_react_docstore_wiki = [
    Tool(
        name="Search",
        description="useful for when you need to ask with search",
        func=docstore_wiki.search
    ),
    Tool(
        name="Lookup",
        description="useful for when you need to ask with lookup",
        func=docstore_wiki.lookup
    )
]

tools_self_ask_with_search = [
    Tool(
        name="Intermediate Answer",
        description="useful for when you need to ask with search",
        func=search_google_serp.run
    )
]

tools_faiss_azure_langchain = [
    Tool(
        name="QA for Azure",
        func=retriev_azure.run,
        description="useful for when you need to query information about Azure disks. Input should be a fully formed question.",
        return_direct=True,
    ),
    Tool(
        name="QA for Langchain",
        func=retriev_langchain.run,
        description="useful for when you need to query information about langchain. Input should be a fully formed question.",
        return_direct=True,
    )
]

tools_faiss_azure_langchain_googleserp = [
    Tool(
        name="QA for Azure",
        func=retriev_azure.run,
        description="useful for when you need to query general information about Azure disks.",
        return_direct=True,
    ),
    Tool(
        name="QA for Langchain",
        func=retriev_langchain.run,
        description="useful for when you need to query information about langchain. Input should be a fully formed question.",
        return_direct=True,
    ),
    Tool(
        name="Search for other information",
        func=search_google_serp.run,
        description="useful for when you need to query about current events and information other than Azure disks and langchain.",
    )
]

