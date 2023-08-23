import os
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List
from pprint import pprint
from langchain.llms import OpenAI
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(model="text-ada-001", temperature=0)


def post_process_bot_response(avatar, user_input, reply_from_llm, profile_output):
    template = (
        "A human and a human-like chatbot named {avatar_name} are having a conversation. You will be provided with an existing bot profile, the user's question, and the bot's response. Analyze the bot's response and provide a summary of any new personal information about the bot that is not already present in the existing bot profile. If no such information is found in the bot's response, simply respond with 'NULL'"
    )
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "existing bot profile : {profile_output} \n user's question: {user_input} \n bot's response: {reply_from_llm}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    # get a chat completion from the formatted messages
    analysis = chat(
        chat_prompt.format_prompt(
            avatar_name=avatar, profile_output=profile_output, user_input=user_input, reply_from_llm=reply_from_llm
        ).to_messages()
    )
    print(
        f"Bot response analysis : \n profile_output : \n {profile_output} \n feed back to profile : \n {analysis.content}")


def save_data_in_bot_profile():
    return


def main(avatar, user_input, reply_from_llm, profile_output):
    post_process_bot_response(avatar, user_input, reply_from_llm, profile_output)


if __name__ == "__main__":
    main()