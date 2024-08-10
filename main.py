import json
import requests
#import pyttsx3
from difflib import get_close_matches
from typing import List, Optional
#from neuralintents.assistants import BasicAssistant

# Initialize the TTS engine
#engine = pyttsx3.init()

todo_list = []

'''def speak(text: str):
    engine.say(text)
    engine.runAndWait()'''

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    matches: List[str] = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def get_weather(api_key: str, location: str = "London") -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"The weather in {location} is currently {weather_description} with a temperature of {temperature}°C."
    else:
        return "Sorry, I couldn't fetch the weather data."

#assistant = BasicAssistant('knowledge_base.json')

#assistant.fit_model(epochs=50)
#assistant.save_model()



def chat_bot():
    api_key = "your_openweathermap_api_key_here"  # Replace with your actual API key
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        if 'add todo list' in user_input.lower():
            print("Bot: What the fuck do you want to add?")
            speak("What the fuck do you want to add?")
            new_data: str = input('Type thing you want to add: ')
            todo_list.append(new_data)

        if 'show todo list to me.' in user_input.lower():
            print(todo_list)
            
            

        if 'weather' in user_input.lower():
            location = "London"  # Default location, can be made dynamic
            weather_info = get_weather(api_key, location)
            print(f'Bot: {weather_info}')
            speak(weather_info)
            continue

        best_match: Optional[str] = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: Optional[str] = get_answer_for_question(best_match, knowledge_base)
            if answer:
                print(f'Bot: {answer}')
                #speak(answer)
            else:
                response = 'I don\'t know the answer.'
                print(f'Bot: {response}')
                #speak(response)
        else:
            response = 'I don\'t know the answer. Can you teach me?'
            print(f'Bot: {response}')
            #speak(response)
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                response = "Thank you! I've learned something new."
                print(f'Bot: {response}')
                #speak(response)

if __name__ == '__main__':
    chat_bot()
   

