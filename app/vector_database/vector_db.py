import os
from datetime import datetime
from pprint import pprint

from dotenv import load_dotenv
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

load_dotenv()

# chroma db detail
chroma_db_base_path = os.environ.get("CHROMA_DB_BASE_PATH")
print("chroma db path: ", chroma_db_base_path)
vectorstore = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory=chroma_db_base_path)

# transformer pattern
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=7,
    chunk_overlap=2
)


def upload_bot_profile(file, bot_id):
    print("upload_bot_profile called")
    # loading data
    raw_documents = TextLoader(file).load()
    documents = text_splitter.split_documents(raw_documents)
    documents_with_header = []
    for doc in documents:
        doc.metadata.__setitem__("bot_id", bot_id)
        doc.metadata.pop("source")
        documents_with_header.append(doc)
        #print(doc)
    vectorstore.add_documents(documents_with_header)


def upload_bot_profile_dir(dir, bot_id):
    print("upload_bot_profile called")
    # loading data
    loader = TextLoader('/data/vikas/Profile/life/Profile.txt')
    print(loader)
    raw_documents = loader.load()
    documents = text_splitter.split_documents(raw_documents)
    documents_with_header = []
    for doc in documents:
        doc.metadata.__setitem__("bot_id", bot_id)
        doc.metadata.pop("source")
        documents_with_header.append(doc)
        #print(doc)
    vectorstore.add_documents(documents_with_header)


def add_bot_profile(data, bot_id):
    print("add_bot_profile called")
    # loading data
    documents = text_splitter.split_documents(data)
    documents_with_header = []
    for doc in documents:
        doc.metadata.__setitem__("bot_id", bot_id)
        doc.metadata.pop("source")
        documents_with_header.append(doc)
    vectorstore.add_documents(documents_with_header)


def fetch_bot_profile(bot_id, query, count):
    print("fetch_bot_profile called")
    #docs = vectorstore.similarity_search(query, k=count, filter={"bot_id": bot_id})
    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.5})
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)
    result = qa({"query": query, "filter": {"bot_id": bot_id}})
    #return docs
    return result['result']


def add_user_profile(data, user_id):
    print("add_user_profile called")
    documents = text_splitter.split_documents(data)
    documents_with_header = []
    for doc in documents:
        doc.metadata.__setitem__("user_id", user_id)
        doc.metadata.pop("source")
        documents_with_header.append(doc)
    vectorstore.add_documents(documents_with_header)


def fetch_user_profile(user_id, query, count):
    print("add_user_profile called")
    docs = vectorstore.similarity_search(query, k=count, filter={"user_id": user_id})
    return docs


def add_conversation(data, bot_id, user_id):
    print("add_user_profile called")
    documents = text_splitter.split_documents(data)
    documents_with_header = []
    for doc in documents:
        doc.metadata.__setitem__("bot_id", bot_id)
        doc.metadata.__setitem__("user_id", user_id)
        doc.metadata.__setitem__("time", datetime.now())
        doc.metadata.pop("source")
        documents_with_header.append(doc)
    vectorstore.add_documents(documents_with_header)


def fetch_conversation(bot_id, user_id, query, count):
    print("add_user_profile called")
    docs = vectorstore.similarity_search(query, k=count, filter={"bot_id": bot_id, "user_id": user_id})
    return docs
