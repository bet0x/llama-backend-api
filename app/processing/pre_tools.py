import openai
import os
from pprint import pprint
from app.vector_database import vector_db
from app.processing import agent
from app.processing import profile


from langchain import SerpAPIWrapper
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature="1.0", model="gpt-3.5-turbo-0613")
function_registry = {}

# Decorator to register functions
def register_function(func_name):
    def decorator(func):
        function_registry[func_name] = func
        return func
    return decorator

@register_function('get_function_photo')
def get_function_photo(nickname,avatar,user_query,chat_history,current_summary):
    return  ("get_function_photo")


@register_function('get_function_profile')
def get_function_profile( nickname,avatar,user_query,chat_history,current_summary):

        ## First try to get the actual question##
        new_message = [{ "role": "system", "content": f"behave like a highly skilled system that  trained in language comprehension and understanding the contexts.  Two humans, named as  '{nickname}' and '{avatar}' are in a casual conversation.Rewrite latest statement by '{nickname}' replacing  all pronouns with appropriate nouns based on the given chat history between the two"},
                { "role": "user", "content": f"the chat history  between the two is '{chat_history}\n\n {nickname}: {user_query}' , now returned only the last modified statement/question." }]
        new_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=new_message,
            temperature=0,
        )
        user_statement = new_response["choices"][0]["message"]["content"]
        profile_data = profile.get_profile(nickname,avatar,user_statement,chat_history,current_summary)
        return  (profile_data)

@register_function('get_function_video')
def get_function_video(nickname,avatar,user_query,chat_history,current_summary):
    return  ("get_function_video")

@register_function('get_function_any_other')
def get_function_any_other(nickname,avatar,user_query,chat_history,current_summary):
    return  ("get_function_any_other")

@register_function('get_function_no_question')
def get_function_no_question(nickname,avatar,user_query,chat_history,current_summary):
    return  ("get_function_no_question")

@register_function('get_function_nothing')
def get_function_nothing(nickname,avatar,user_query,chat_history,current_summary):
    return  ("get_function_nothing")


def search_docs(ques, chat_history, nickname, avatar):
    function_name = agent.get_function(nickname,avatar,ques,chat_history,"")
    profile_output=""
    if function_name in function_registry:
         # Get the function from the registry
           selected_function = function_registry[function_name]
           current_summary = ""
        # Call the selected function
           profile_output = selected_function(nickname,avatar,ques,chat_history,current_summary)
           print(f" is {profile_output}")

    return profile_output

