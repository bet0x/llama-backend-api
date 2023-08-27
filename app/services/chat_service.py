import requests
from flask import jsonify
from langchain import OpenAI
from werkzeug.datastructures import MultiDict
from dotenv import load_dotenv , find_dotenv
from app.models.database_models import ChatMessage
from app.processing import pre_processing, pre_tools
from app.repository.chat_repository import get_chat_history_by_bot_id_and_user_id, get_session_chat_history, \
    get_chat_history_by_bot_id_and_user_id_timestamp, save_chat_message , delete_chat_history
from app.services import avatar_service
import os
import base64
from app.logger import get_logger
load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY= os.getenv("ELEVEN_LABS_API_KEY")

logger = get_logger(__name__)


def chat(chat_message: ChatMessage):
    # bot_id, user_id, name, message, _id, session_id, is_user_message, is_deleted, timestamp -> coming from FE
    user_save_resp = save_chat_message(chat_message)
    print("user_save_resp", user_save_resp)
    logger.info(f"user_save_resp: {user_save_resp}")

    avatar = avatar_service.get_bot_name_by_bot_id(chat_message.bot_id)
    print("avatar name: ", avatar)
    logger.info(f"avatar name:: {avatar}")

    chat_hist = pre_processing.format_chat_history(chat_message.bot_id, chat_message.user_id)
    print("chat_history: ", chat_hist)
    logger.info(f"chat_history: {chat_hist}")

    profile_output = pre_tools.search_docs(chat_message.message, chat_hist, chat_message.name, avatar,
                                           chat_message.bot_id)
    print("profile_output: ", profile_output)
    logger.info(f"profile_output: {profile_output}")

    body_data = pre_processing.llama_prompt(avatar, chat_message.name, profile_output, chat_hist, chat_message.message)
    print("preprocess_output :", body_data)
    logger.info(f"preprocess_output: {body_data}")
    ip_address = "127.0.0.1"
    port = 8000  # Replace with the actual port number

    api_url = f"http://{ip_address}:{port}/v1/completions"
    response = requests.post(
        url=api_url,
        json=body_data,
        headers={"content-type": "application/json"}
    )

    # response = get_response_from_openai(preprocess_output)
    response_data = response.json()
    print("Response: ", response_data)
    logger.info(f"Response: {response_data}")
    final_response = response_data["choices"][0]["text"]
    print(f"final response is {final_response}")
    logger.info(f"final response is {final_response}")
    base64_audio = get_voice_message(final_response)
    # print("base64 audio", base64_audio)
    print(f"final response is {final_response}")
    ai_chat_msg = ChatMessage(bot_id=chat_message.bot_id, user_id=chat_message.user_id, message=final_response,
                              is_user_message=False, session_id=chat_message.session_id,
                              query_type=chat_message.query_type)
    ai_save_resp = save_chat_message(ai_chat_msg)
    print("ai_save_resp", ai_save_resp)
    logger.info(f"ai_save_resp: {ai_save_resp}")
    print(f"chat ai_chat_msg --> {ai_chat_msg}")
    logger.info(f"ai_chat_msg: {ai_chat_msg}")
    # post_processing.main(avatar, chat_message.message, final_response, profile_output)  # make it background process
    return jsonify({
        "user_id": chat_message.user_id,
        "bot_id": chat_message.bot_id,
        "resp_type": chat_message.query_type,
        "resp_msg": final_response,
        "resp_url": "hardcoded_url",
        "timestamp": ai_chat_msg.timestamp,
        "audio_base64": base64_audio
    })


def upload_image():
    return


# function to get chat history by bot_id and user_id to display in chat history page
def chat_history(args: MultiDict[str, str]):
    print("chat_history", args)
    logger.info(f"chat_history: {args}")
    bot_id = args.get("bot_id", None)
    user_id = args.get("user_id", None)
    limit = int(args.get("limit", 10))
    timestamp = int(args.get("timestamp", 0))
    offset = int(args.get("offset", 0))
    mode = args.get("mode", "before")

    if timestamp > 0:
        return chat_history_with_timestamp(bot_id, user_id, limit, mode, timestamp)
    else:
        history = get_chat_history_by_bot_id_and_user_id(bot_id, user_id, limit, offset)
        return jsonify(history)


def chat_history_with_timestamp(bot_id: str, user_id: str, limit: int = 10, mode: str = "before", timestamp: int = 0):
    history = get_chat_history_by_bot_id_and_user_id_timestamp(bot_id, user_id, limit, timestamp, mode)
    return jsonify(history)


def chat_session_history(bot_id: str, user_id: str, session_id: str):
    history = get_session_chat_history(bot_id, user_id, session_id)
    return jsonify(history)


def delete_chat(bot_id: str, user_id: str):
    logger.info(f"delete_chat: {bot_id}, {user_id}")
    result = delete_chat_history(bot_id, user_id)
    if result == True:
        return jsonify({
            "message": "chats have been deleted"
        })
    else:
        return jsonify({
            "message": "something went wrong"
        }), 500    



def download():
    return


# function to get context from history message based on last session id
def get_context_from_history(bot_id, user_id):
    logger.info(f"get_context_from_history: {bot_id}, {user_id}")
    return None


# function to pre-process data before sending to OpenAI and return a final prompt for OPENAI to generate response
def preprocess(chat_message: ChatMessage):
    print("Preprocessing...", chat_message)
    logger.info(f"Preprocessing: {chat_message}")
    avatar = avatar_service.get_bot_name_by_bot_id(chat_message.bot_id)
    prompt = pre_processing.query_to_llm(chat_message.message, chat_message.bot_id, chat_message.user_id,
                                         chat_message.name, avatar)
    return prompt


def post_process(response):
    logger.info(f"Postprocessing: {response}")
    return response


def get_response_from_openai(preprocess_output):
    # if type(preprocess_output) is ChatMessage:
    try:
        llm = OpenAI(temperature="1.0")
        print("making openai call: ", preprocess_output)
        logger.info(f"making openai call: {preprocess_output}")
        openai_response = llm(preprocess_output)
        print("OpenAI response: ", str(openai_response))
        logger.info(f"OpenAI response:: {str(openai_response)}")
        return openai_response
    except Exception as e:
        print("OpenAI error: ", str(e))
        logger.info(f"OpenAI error:: {str(e)}")
        return "Sorry, I don't understand. Can you please rephrase?"


def get_voice_message(message):
    payload = {
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0,            
            "similiarity_boost": 0
        }
    }


    headers = {
        "accept": 'audio/mpeg',
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": 'application/json'
    }

    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM?optimize_streaming_latency=0' ,
                            json=payload,
                            headers=headers)
    



    if response.status_code == 200 and response.content:
        base64_encoded_audio = base64.b64encode(response.content).decode('utf-8')
        return base64_encoded_audio
    else:
        return None
