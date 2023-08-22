import openai
from pydantic import BaseModel
import json



#base_model: Optional[BaseModel] = None
#base_model_schema = base_model.schema()

def get_function_photo(question):

      what_to_do = {
             "question":question,
             }

      return json.dumps(what_to_do) 

def get_function_profile(question ):
      what_to_do = {
             "question":question,
             }

      return json.dumps(what_to_do) 


def get_function_no_question(question):
      what_to_do = {
             "question":question,
             }

      return json.dumps(what_to_do) 

def get_function_video(question):
      what_to_do = {
             "question":question,
             }

      return json.dumps(what_to_do) 

def get_function_any_other(question):
      what_to_do = {
             "question":question,
             }

      return json.dumps(what_to_do) 

functions = [
        {
            "name": "get_function_photo",
            "description": "if in the current statement of human1, he/she is  is looking for a picture ",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "which respect to which human ",
                    }
                },
                "required": ["question"],
            },
        },
        {
            "name": "get_function_profile",
            "description": " in the current statment of human1 , if human1  wanted to know anything associated with human2, also change the question or statement,  pronouns  are replaced by nouns by considering the the chat summary and history",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "  the  changed question or statement ",
                    }
                },
                "required": ["question"],
            },
        },
        {
            "name": "get_function_no_question",
            "description": "if in the current statment of   human1, human1 is not is not asking any question about Human2 or related to human2  ",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "with respet to which human",
                    }
                },
                "required": ["question"],
            },
        },
        {
            "name": "get_function_any_other",
            "description": "for all the other conditions.if nothing else match treat it as defalut function  ",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "with respet to which human",
                    }
                },
                "required": ["question"],
            },
        },
        {
            "name": "get_function_video",
            "description": "if human1 wants human2 to send her video  ",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "with respet to which human",
                    }
                },
                "required": ["question"],
            },
        }
    ]

#function_params = {
#            "name": base_model_schema["title"],
#            "description": base_model_schema["description"]
#            if "description" in base_model_schema
#            else None,
#            "parameters": base_model_schema,
#        }



def get_function(nickname, avatar, user_query, chat_history,current_summary):

     transcription = f"{chat_history} \n {user_query}"
     messages = [{"role": "user", "content": f"behave like  a highly skilled AI trained in language comprehension and understanding the contexts. Read the following conversation between  human1  as {nickname}: and human2 as {avatar}: with their chat history as {chat_history} and the current  statement of  {nickname} is  {user_query}"}]


     response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=messages,
            functions=functions,
            function_call="auto",
        )
     response_message = response["choices"][0]["message"]
     #print (response_message)

     if response_message.get("function_call"):
        print(response_message["function_call"]["name"])
        function_args = json.loads(response_message["function_call"]["arguments"])
        question=function_args.get("question"),

        #"""let's correct the question"""#
        #new_message = [{ "role": "system", "content": f"behave like a highly skilled system that  trained in language comprehension and understanding the contexts.  Two humans, named as  '{nickname}' and '{avatar}' are in a casual conversation.Rewrite latest statement by '{nickname}' replacing  all pronouns with appropriate nouns based on the given chat history between the two"},
        #        { "role": "user", "content": f"the chat history  between the two is '{chat_history}\n\n {nickname}: {user_query}' , now returned only the last modified statement/question." }]
        #print(new_message)
        #new_response = openai.ChatCompletion.create(
        #    model="gpt-3.5-turbo",
        #    messages=new_message,
        ##    temperature=0,
        #)

        #print(new_response)

        return (response_message["function_call"]["name"])
     else:
         return ("get_function_nothing")

    
     return response
    

def get_current_question( nickname, avatar, user_query, chat_history):
    transcription = f"  {chat_history} \n {user_query}"

    # Use GPT-3 to generate the response based on the prompt

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "srstem",
                "content": f"behave like a expert in language comprehension and understanding the context. I would like you to read the following   conversation between two human  defined as {nickname}: and {avatar}: in provided text. you have to return the current unasnwered question of  {nickname}."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )

    response = response.choices[0].text.strip()
    return response['choices'][0]['message']['content']
