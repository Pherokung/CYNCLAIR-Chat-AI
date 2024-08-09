#a ensemble retriever of BM25 and vector store for ranking 

import os

from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.output_parsers import StrOutputParser

from basic_chain import get_model
#from rag_chain import make_rag_chain
from vector_store import create_vector_db
from dotenv import load_dotenv


def ensemble_retriever_from_docs(texts, embeddings=None):
    vs = create_vector_db(texts, embeddings)
    vs_retriever = vs.as_retriever()

    bm25_retriever = BM25Retriever.from_texts([t.page_content for t in texts])

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vs_retriever],
        weights=[0.5, 0.5])

    return ensemble_retriever