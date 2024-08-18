import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import WikipediaLoader

try:
    base = Path(__file__).parent.parent
    directory_path = base / 'CVE_Database' / 'CVE_MD'

except:
    print("Error: Cannot file the folder CVE_MD")


def list_md_files(data_dir = directory_path):
    paths = Path(data_dir).glob('**/*.md')
    for path in paths:
        yield str(path)


def load_md_files(data_dir = directory_path):
    docs = []
    paths = list_md_files(data_dir)
    for path in paths:
        print(f"Loading {path}")
        loader = TextLoader(path)
        docs.extend(loader.load())
    
    return docs

"""
def get_wiki_docs(query, load_max_docs=2):
    wiki_loader = WikipediaLoader(query=query, load_max_docs=load_max_docs)
    docs = wiki_loader.load()
    for d in docs:
        print(d.metadata["title"])
    return docs
"""
