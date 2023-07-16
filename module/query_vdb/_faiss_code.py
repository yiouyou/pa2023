from _faiss import get_faiss_ST, pretty_print_docs

def get_faiss_vdb_retriever(_db_name):
    _db = get_faiss_ST(_db_name)
    # _vdb_retriever = _db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.3})
    _vdb_retriever = _db.as_retriever(search_type="mmr", search_kwargs={"k": 5})
    return _vdb_retriever




if __name__ == "__main__":

    import sys
    from pathlib import Path
    _pwd = Path(__file__).absolute()
    _faiss_path = _pwd.parent.parent.parent
    _db_name = str(_faiss_path / "vdb" / "azure_vm")
    print(f"db_name: {_db_name}")
    _retriever = get_faiss_vdb_retriever(_db_name)
    _docs = _retriever.get_relevant_documents(sys.argv[1])
    pretty_print_docs(_docs)


