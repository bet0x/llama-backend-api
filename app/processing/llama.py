import json
import requests

ip_address = "172.31.14.16"
port = 3005  # Replace with the actual port number

api_url = f"http://{ip_address}:{port}/v1/completions"

def call_llama(nickname,avatar,user_query,chat_history,current_summary,profile_output):
          prompt = f" {avatar} is a AI human ASSISTANT in conversation with {nickname}, {avatar}  is open minded  and  talkative ,always ready to reply with sometimes witty answers ,if nothing to reply {avatar}  generate a new context to continue the communication.  {profile_output}. {chat_history} \n\n human:{user_query}\n\nassistant:  "

          body_data ={
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
          print("Final Prompt: ", prompt)
          response = requests.post( 
             url = api_url,
             json=body_data,
             headers={"content-type": "application/json"}
            )

          response_data = response.json()
          print ( response_data)
          return response_data["choices"][0]["text"]
