import re

from langchain import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from app.vector_database import vector_db
from app.logger import get_logger


logger = get_logger(__name__)

embeddings = OpenAIEmbeddings()


def get_profile(nickname, avatar, user_query, chat_history, current_summary, bot_id):
    print(f"query is {user_query}")
    logger.info(f"query is {user_query}")
    query = result = re.sub(r'^.*?:', '', user_query, count=1)
    # found_docs = qdrant.similarity_search(query)
    llm = OpenAI()
    # retriever =qdrant.as_retriever( search_type="mmr", search_kwargs={'k': 2, 'fetch_k': 50})

    #  retriever = qdrant.as_retriever(search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.5})

    # qa = RetrievalQA.from_chain_type(
    #        llm=OpenAI(),
    #       chain_type="stuff",
    #   retriever= retriever,
    #   return_source_documents=True
    #   )

    # result = qa({"query": query})
    # print(result['result'])
    result = vector_db.fetch_bot_profile(bot_id, query, 5)
    return result
