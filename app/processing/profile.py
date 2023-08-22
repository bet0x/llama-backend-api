import torch
import re
from sentence_transformers import models,SentenceTransformer,util
import os
import glob
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.document_loaders import TextLoader
from langchain import OpenAI
from langchain.chains import RetrievalQA

embeddings = OpenAIEmbeddings()


def load_sentences_from_files():
    loader = TextLoader("/data/vikas/Profile/life/Profile.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    return docs

docs = load_sentences_from_files()

qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    path="/tmp/docs",
    collection_name="Profile",
)

def get_profile(nickname,avatar,user_query,chat_history,current_summary):

        print ( f"query is {user_query}")
        query = result = re.sub(r'^.*?:', '', user_query, count=1) 
        #found_docs = qdrant.similarity_search(query)
        llm = OpenAI()
        #retriever =qdrant.as_retriever( search_type="mmr", search_kwargs={'k': 2, 'fetch_k': 50})

        retriever = qdrant.as_retriever(search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.5})

        qa = RetrievalQA.from_chain_type(
                llm=OpenAI(), 
                chain_type="stuff", 
                retriever= retriever,
                return_source_documents=True
                )

        result = qa({"query": query})
        print(result['result'])

        return(result['result'])
