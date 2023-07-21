from ._web import txt2name, clean_txt, get_docs_from_links, split_docs_recursive

def embedding_to_faiss_ST(_docs, _db_name):
    from langchain.vectorstores import FAISS
    from langchain.embeddings import HuggingFaceEmbeddings
    _embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2") # all-mpnet-base-v2/all-MiniLM-L6-v2/all-MiniLM-L12-v2
    _db = FAISS.from_documents(_docs, _embeddings)
    _db.save_local(_db_name)
    print(_db_name)
    print("[faiss save HuggingFaceEmbeddings embedding to disk]")

def embedding_to_faiss_OpenAI(_docs, _db_name):
    from langchain.vectorstores import FAISS
    from langchain.embeddings.openai import OpenAIEmbeddings
    from dotenv import load_dotenv
    load_dotenv()
    _embeddings = OpenAIEmbeddings()
    _db = FAISS.from_documents(_docs, _embeddings)
    _db.save_local(_db_name)
    print("[faiss save OpenAI embedding to disk]")

def weblinks_to_faiss(_links, _db_name):
    docs = get_docs_from_links(_links)
    if len(docs) > 0:
        for doc in docs:
            doc.page_content = clean_txt(doc.page_content)
            # print(doc.metadata)
        print(f"docs: {len(docs)}")
        splited_docs = split_docs_recursive(docs)
        print(f"splited_docs: {len(splited_docs)}")
        embedding_to_faiss_ST(splited_docs, _db_name)
    else:
        print("NO docs")

def url_recursive_to_faiss(_url, _exclude, _db_name):
    import nest_asyncio
    nest_asyncio.apply()
    from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
    loader = RecursiveUrlLoader(url=_url, exclude_dirs=_exclude)
    loader.verify = False
    loader.requests_per_second = 1
    docs=loader.load()
    if len(docs) > 0:
        for doc in docs:
            doc.page_content = clean_txt(doc.page_content)
            print(doc.metadata)
        print(f"docs: {len(docs)}")
        splited_docs = split_docs_recursive(docs)
        print(f"splited_docs: {len(splited_docs)}")
        embedding_to_faiss_ST(splited_docs, _db_name)
    else:
        print("NO docs")

def weblinks_to_link_md(_links, _dir):
    import re, os, json
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    import requests
    from markdownify import markdownify
    with open(_links, "r") as lf:
        _list = lf.read().splitlines()
    n = 0
    link_md = {}
    for i in _list:
        n += 1
        print(i)
        _r = requests.get(i)
        _t1 = markdownify(_r.text, heading_style="ATX")
        _t2 = re.sub(r'\n\s*\n', '\n\n', _t1)
        _t3 = _t2.split("\nTable of contents\n\n")
        _t4 = _t3[-1]
        _t5 = _t4.split("\n## Additional resources\n\n")
        _t6 = _t5[0]
        _t7 = _t6.split("\nTheme\n\n")
        _t8 = _t7[0]
        fn = os.path.join(_dir, f"{str(n).zfill(3)}.md")
        print(fn)
        with open(fn, "w") as wf:
            wf.write(_t8)
        link_md[fn] = i
    # print(link_md)
    fn = os.path.join(_dir, "_link_md.json")
    with open(fn, "w", encoding="utf-8") as wf:
        wf.write(json.dumps(link_md, ensure_ascii=False, indent=4))

def link_md_to_faiss(_dir, _db_name):
    import os, json
    from langchain.text_splitter import MarkdownHeaderTextSplitter
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        # ("####", "Header 4"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    _docs = []
    fn = os.path.join(_dir, "_link_md.json")
    with open(fn, "r", encoding="utf-8") as rf:
        link_md = json.loads(rf.read())
    # print(link_md)
    for i in link_md:
        print(i)
        with open(i, "r", encoding="utf-8") as rf:
            _t = rf.read()
            _md = markdown_splitter.split_text(_t)
            for j in _md:
                _m1 = j.metadata
                _headers = _m1.values()
                _m1['description'] = ', '.join(_headers)
                _m1['source'] = link_md[i]
                j.metadata = _m1
            _docs += _md
    print(f"docs: {len(_docs)}")
    embedding_to_faiss_ST(_docs, _db_name)


if __name__ == "__main__":

    from _web import txt2name, clean_txt, get_docs_from_links, split_docs_recursive
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _faiss_path = _pwd.parent.parent.parent

    # _db_azure = txt2name("Azure VM")
    # print(_db_azure)
    # _links = str(_faiss_path / "vdb" / "azure_vm.link")
    # _azure = str(_faiss_path / "vdb" / _db_azure)
    # _md_dir = "./md_azure_vm"
    # weblinks_to_link_md(_links, _md_dir)
    # link_md_to_faiss(_md_dir, _azure)

    _db_azure = txt2name("Azure SQL+")
    print(_db_azure)
    _links = str(_faiss_path / "vdb" / "azure_sql+.link")
    _azure = str(_faiss_path / "vdb" / _db_azure)
    _md_dir = "./md_azure_sql+"
    weblinks_to_link_md(_links, _md_dir)
    link_md_to_faiss(_md_dir, _azure)

    # _db_azure = txt2name("Azure WebApps")
    # print(_db_azure)
    # _links = str(_faiss_path / "vdb" / "azure_webapps.link")
    # _azure = str(_faiss_path / "vdb" / _db_azure)
    # _md_dir = "./md_azure_webapp"
    # weblinks_to_link_md(_links, _md_dir)
    # link_md_to_faiss(_md_dir, _azure)

    # _db_langchain = txt2name("Langchain Python Documents")
    # print(_db_langchain)
    # _url = 'https://python.langchain.com/docs/modules/'
    # _exclude = [
    #     'https://python.langchain.com/docs/additional_resources',
    #     'https://api.python.langchain.com/en/latest/',
    # ]
    # _langchain = str(_faiss_path / "vdb" / _db_langchain)
    # url_recursive_to_faiss(_url, _exclude, _langchain)

