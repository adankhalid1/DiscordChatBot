from random import choice, randint
import datetime
import discord
import requests
import os
import openai
from discord.ext import commands


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return get_greeting()
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'my name' in lowered:
        return "Your name is your secret identity!"
    elif 'thank you' in lowered or 'thanks' in lowered:
        return "You're welcome! 😊"
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'
    elif 'flip coin' in lowered:
        return f'The coin landed on: {choice(["heads", "tails"])}'
    elif 'time' in lowered:
        return get_current_time()
    elif 'date' in lowered:
        return get_current_date()
    elif 'predict' in lowered:
        return get_prediction()
    elif 'your favorite' in lowered:
        return get_favorite(lowered)
    elif any(word in lowered for word in ['great', 'awesome', 'amazing']):
        return get_compliment()
    elif 'tell me a joke' in lowered:
        return get_joke()
    elif 'chuck norris' in lowered:
        joke_info = get_chuck_norris_joke()
        return joke_info
    elif 'random pic' in lowered:
        pic_info = get_random_image()
        return pic_info
    elif 'advice' in lowered:
        advice_info = get_advice()
        return advice_info
    elif 'weather' in lowered:
        return 'The weather is sunny with a chance of rain later.'
    elif 'add' in lowered or 'subtract' in lowered or 'multiply' in lowered or 'divide' in lowered:
        return handle_math(lowered)
    elif 'faq' in lowered:
        return get_faq(lowered)
    elif 'chatgpt' in lowered:
        return get_chatgpt_response(user_input)  # Calls ChatGPT API
    elif 'commands' in lowered or 'help' in lowered:
        return """Available commands:
- Hello
- How are you
- Bye
- My name
- Thank you / Thanks
- Roll dice
- Flip coin
- Time
- Date
- Predict
- Your favorite (e.g., your favorite color)
- Great / Awesome / Amazing
- Tell me a joke
- Weather
- Add (e.g., add 5 and 3)
- Subtract (e.g., subtract 10 from 7)
- Multiply (e.g., multiply 4 by 6)
- Divide (e.g., divide 8 by 2)
- FAQ (e.g., faq about name, faq about created, faq about do)
"""
    elif 'countdown' in lowered:
        return get_countdown(lowered)
    elif 'fact' in lowered:
        return get_random_fact()
    elif 'echo' in lowered:
        return echo(user_input)
    else:
        return choice(['I do not understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?'])

def get_greeting() -> str:
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        return 'Good morning!'
    elif 12 <= current_hour < 18:
        return 'Good afternoon!'
    else:
        return 'Good evening!'

def get_current_time() -> str:
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    return f"The current time is {current_time}."

def get_current_date() -> str:
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    return f"Today's date is {current_date}."

def get_prediction() -> str:
    predictions = [
        "You will have a great day!",
        "A surprise is waiting for you around the corner.",
        "Beware of unexpected meetings today.",
        "Luck is on your side!"
    ]
    return choice(predictions)

def get_favorite(lowered: str) -> str:
    favorites = {
        'color': 'Purple my favorite color!',
        'food': 'Sumaq Shawarma slaps.',
        'activity': 'Chatting with you, of course!',
        'movie': 'I love spiderman.'
    }
    for key, response in favorites.items():
        if key in lowered:
            return response
    return "I have many favorites, ask me about a specific one!"

def get_compliment() -> str:
    compliments = [
        "Thank you! You're pretty awesome too!",
        "Aw, shucks! Thanks!",
        "You're making me blush!"
    ]
    return choice(compliments)

def get_joke() -> str:
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I told my wife she should embrace her mistakes. She gave me a hug.",
        "Parallel lines have so much in common. It’s a shame they’ll never meet.",
        "Why do we never tell secrets on a farm? Because the potatoes have eyes and the corn has ears.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "I used to play piano by ear, but now I use my hands.",
        "I told my computer I needed a break and now it won't stop laughing.",
        "I'm on a seafood diet. I see food and I eat it."
    ]
    return choice(jokes)

def handle_math(lowered: str) -> str:
    try:
        parts = lowered.split()
        numbers = [float(part) for part in parts if part.replace('.', '', 1).isdigit()]
        if len(numbers) < 2:
            return 'Please provide at least two numbers for the operation.'

        if 'add' in lowered:
            result = sum(numbers)
            return f'The sum is {result}.'
        elif 'subtract' in lowered:
            result = numbers[0] - numbers[1]
            return f'The difference is {result}.'
        elif 'multiply' in lowered:
            result = numbers[0] * numbers[1]
            return f'The product is {result}.'
        elif 'divide' in lowered:
            if numbers[1] == 0:
                return 'Cannot divide by zero.'
            result = numbers[0] / numbers[1]
            return f'The quotient is {result}.'
    except (IndexError, ValueError):
        return 'Please provide valid numbers for the operation.'

def get_faq(lowered: str) -> str:
    faq_responses = {
        'name': 'I am your friendly bot!',
        'created': 'I was created by a talented developer.',
        'do': 'I can chat with you, tell jokes, do basic math, and more!'
    }
    for keyword, response in faq_responses.items():
        if keyword in lowered:
            return response
    return 'I am not sure how to answer that FAQ.'

def get_countdown(lowered: str) -> str:
    try:
        parts = lowered.split()
        target_date_str = next((word for word in parts if '/' in word), None)
        if not target_date_str:
            return 'Please specify a date in the format MM/DD/YYYY.'
        target_date = datetime.datetime.strptime(target_date_str, '%m/%d/%Y')
        current_date = datetime.datetime.now()
        days_left = (target_date - current_date).days
        return f"There are {days_left} days left until {target_date_str}."
    except ValueError:
        return 'Please specify a valid date in the format MM/DD/YYYY.'

def get_random_fact() -> str:
    facts = [
        "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion of iron.",
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "Octopuses have three hearts. Two pump blood to the gills, while the third pumps it to the rest of the body."
    ]
    return choice(facts)

def get_chuck_norris_joke() -> str:
    url = 'https://api.chucknorris.io/jokes/random'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        icon_url = "https://api.chucknorris.io/img/avatar/chuck-norris.png"
        joke_id = data['id']
        joke_url = data['url']
        joke_value = data['value']
        return f"Chuck Norris Joke:\n{joke_value}\n\nID: {joke_id}\nURL: {joke_url}\nIcon: {icon_url}"
    else:
        return 'Failed to fetch Chuck Norris joke. Try again later.'

def get_random_image() -> str:
    url = 'https://picsum.photos/200/300'  # Adjust the URL to your preferred image size or parameters
    response = requests.get(url)
    if response.status_code == 200:
        image_url = response.url
        return image_url
    else:
        return 'Failed to fetch image. Try again later.'
    
def get_advice() -> str:
    url = 'https://api.adviceslip.com/advice'
    response = requests.get(url)
    if response.status_code == 200:
        advice = response.json()['slip']['advice']
        return advice
    else:
        return 'Could not fetch advice at this time.'

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatgpt_response(user_input: str) -> str:
    try:
        # Make a request to OpenAI's ChatGPT API
        response = openai.Completion.create(
            model="text-davinci-003",  # You can adjust this model as per your needs
            prompt=user_input,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error with OpenAI API: {str(e)}"
    

def echo(user_input: str) -> str:
    return f"You said: '{user_input}'"
