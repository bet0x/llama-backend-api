from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from app.processing.pre_tools import search_docs
from app.repository.chat_repository import get_chat_history_by_bot_id_and_user_id
from app.services.avatar_service import get_bot_name_by_bot_id
from app.vector_database import vector_db

text_splitter = CharacterTextSplitter(separator="\n", chunk_size=5, chunk_overlap=1)
embeddings = OpenAIEmbeddings()

# Persist on Vector
# vectorstore = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="D:\\ChromaDb")

llm = ChatOpenAI(temperature="1.0", model="gpt-3.5-turbo-0613")

# ChatOpenAI(model="text-ada-001", temperature=0.2)

llm_prompt_template = """
    You are an AI assistant model mimicking human behaviour. Use your knowledge and try to understand the context to answer user queries. If you don't know the answer, reply politely that you don't know , try to be as human as possible
    in your answers.

    Bot also has a profile stored in a vector database which returned the following answer when queried.

    Vector_profile: {profile}

    Context: {context}

    Question: {question}

    Now answer the user question based on the provided information.

    Answer:
"""

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chat_hist = []
chat_summary = ""


def main(message, bot_id, user_id, name):
    print("Main Function")
    # load_bot_profile()
    # add_new_bot_profile()
    avatar = get_bot_name_by_bot_id(bot_id)
    prompt = query_to_llm(message, bot_id, user_id, name, avatar)
    return prompt


def llama_prompt(avatar, nickname, profile_output, chat_history, user_query):
    print("llama prompt called")
    prompt = f" {avatar} is a AI human ASSISTANT in conversation with {nickname}, {avatar}  is open minded  and  talkative ,always ready to reply with sometimes witty answers ,if nothing to reply {avatar}  generate a new context to continue the communication. This is the output from the assistant profile - {profile_output}. This is the recent chat history between the two {chat_history} \n\n Human:{user_query}\n\nAssistant:  "
    body_data = {
        "prompt": prompt,
        "stop": "[</s>]",
        "max_tokens": 100,
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "avatar": avatar,
        "user": nickname,
    }
    return body_data


def query_to_llm(user_query, bot_id, user_id, nickname, avatar):
    print("Query to LLM")
    chat_history = format_chat_history(bot_id, user_id)
    print("chat_history: ", chat_history)
    profile_output = search_docs(user_query, chat_history, nickname, avatar, bot_id)
    print("profile_output: ", profile_output)
    prompt = f" {avatar} is a AI human ASSISTANT in conversation with {nickname}, {avatar}  is open minded  and  talkative ,always ready to reply with sometimes witty answers ,if nothing to reply {avatar}  generate a new context to continue the communication.  {profile_output}. {chat_history} \n\n Human:{user_query}\n\nAssistant:  "
    body_data = {
        "prompt": prompt,
        "stop": "[</s>]",
        "max_tokens": 100,
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "avatar": avatar,
        "user": nickname,
    }

    # prompt = set_prompt_template()
    # context = ''
    # context = get_chat_context(chat_history)

    # llm_prompt = prompt.format(profile=res, context=context, question=user_prompt)
    # print(chat_history)
    # chat_summ = summarize_chat(chat_history)
    return body_data


def summarize_chat(chat_history):
    print("Summary Chat")
    summary_prompt = """
        You are experienced in summarizing chats between two persons. Now take this chat between two users and summarize it in not more than 100 words. 
        Chat History - {chat_hist}
    """
    prompt = PromptTemplate(template=summary_prompt, input_variables=['chat_hist'])
    sum_chain = LLMChain(llm=llm, prompt=prompt, verbose=True, output_key='summary_script')
    summ = sum_chain.run(chat_hist=chat_history)
    # return context
    print(summ)
    return summ


def get_chat_context(chat_summ):
    print("get_chat_context()")
    chat_context_prompt = """
    This is the chat between two users. {chat_summ}. Please provide me with the context about which this chat is going on. If in between chats the context seems to be changing provide me with new context.
    """
    prompt = PromptTemplate(template=chat_context_prompt, input_variables=['chat_summ'])
    chat_context = LLMChain(llm=llm, prompt=prompt, verbose=True, output_key='summary_script')
    context = chat_context.run(chat_summ=chat_summ)
    # return context
    print(context)
    return context


def set_prompt_template():
    # prompt = PromptTemplate(template=llm_prompt_template, input_variables=['context', 'question', 'profile'])
    prompt = PromptTemplate.from_template(llm_prompt_template)
    return prompt


def load_bot_profile():
    print("Loading Bot Profile")
    # loader = DirectoryLoader('profiles/', glob='**/*.txt')
    loader = TextLoader('profiles/Anastasia_profile.txt')
    document = loader.load()
    # print(len(document))
    # print(document)
    load_docs_to_vector(document)


def load_docs_to_vector(document):
    print("Loading documents to vector")
    texts = text_splitter.split_documents(document)
    print(len(texts))
    print(texts)
    db = Chroma.from_documents(texts, OpenAIEmbeddings())


def add_new_bot_profile():
    print("Adding new bot profile")

    vector_db.upload_bot_profile_dir('yo', 1)


def format_chat_history(bot_id, user_id):
    print("format_chat_history For Bot and User : ", bot_id, user_id)
    chat_histories = get_chat_history_by_bot_id_and_user_id(bot_id, user_id)
    formatted_messages = []
    for history in reversed(chat_histories):
        # print(chat)
        message = history['message']
        if history['is_user_message']:
            formatted_messages.append(f"Human: {message}")
        else:
            formatted_messages.append(f"Assistant: {message}")
    return formatted_messages
