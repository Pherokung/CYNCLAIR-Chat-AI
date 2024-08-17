#a ensemble retriever of BM25 and vector store for ranking 

import os

from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter, LongContextReorder
from langchain_community.embeddings import HuggingFaceBgeEmbeddings, HuggingFaceEmbeddings
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever, MergerRetriever
from langchain.chains import RetrievalQA

from functions.basic_chain import get_model
from functions.rag_chain import make_rag_chain
from functions.vector_store import create_vector_db
from dotenv import load_dotenv


def ensemble_retriever_from_docs(texts, embeddings=None):
    dense_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    sparse_embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-large-en",
                                                 encode_kwargs={'normalize_embeddings': False})
    dense_vs = create_vector_db(texts, collection_name="dense", embeddings=dense_embeddings)
    sparse_vs = create_vector_db(texts, collection_name="sparse", embeddings=sparse_embeddings)
    vector_stores = [dense_vs, sparse_vs]

    emb_filter = EmbeddingsRedundantFilter(embeddings=sparse_embeddings)
    reordering = LongContextReorder()
    pipeline = DocumentCompressorPipeline(transformers=[emb_filter, reordering])

    base_retrievers = [vs.as_retriever() for vs in vector_stores]
    lotr = MergerRetriever(retrievers=base_retrievers)

    compression_retriever_reordered = ContextualCompressionRetriever(
        base_compressor=pipeline, base_retriever=lotr, search_kwargs={"k": 5, "include_metadata": True}
    )
    return compression_retriever_reordered