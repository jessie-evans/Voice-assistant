import pyttsx3
import wikipedia
import speech_recognition as sr
import datetime
import pywhatkit
import webbrowser
import requests

engine = pyttsx3.init()
recognizer = sr.Recognizer()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Clearing the background noises... Please wait")
        print("Listening...")

        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
                text = recognizer.recognize_google(audio, language='en_US')
                print("You said:", text)
                return text.lower()
            except sr.UnknownValueError:
                print("Listening again...")  
            except sr.RequestError:
                print("Sorry, there was a problem with the service.")
                speak("Sorry, there was a problem with the service.")
                break

def process_command(command):
    if 'hello' in command:
        speak("Hello, how can I help you?")
    elif 'ok jarvis' in command:
        speak("Hello, how can I help you?")
    elif 'name' in command:
        speak("My name is Jarvis")
    elif 'jarvis' in command:
        speak("It is an Intelligent System")
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print("Current time:", time)
        speak(f"The time is {time}")
    elif 'play' in command:
        song = command.replace('play', '').strip()  
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)  
    elif "search" in command:
        speak("What would you like to search for?")
        query = listen()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Here are the results for {query}.")
    elif 'explain' in command:
        topic = command.replace('explain', '').strip()
        result = wikipedia.summary(topic, sentences=3)
        print(result)
        speak(result)
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'weather' in command:
        speak("Please tell me the city name.")
        cityname = listen()
        apiKey = "7040ea904442a45d6950ba584410ce59"
        baseURL = "http://api.openweathermap.org/data/2.5/weather?q="
        completeURL = baseURL + cityname + "&appid=" + apiKey
        response = requests.get(completeURL)
        data = response.json()
        if data["cod"] != "404":
            main = data["main"]
            wind = data["wind"]
            temperature = main["temp"]
            humidity = main["humidity"]
            wind_speed = wind["speed"]
            weather_desc = data["weather"][0]["description"]
            weather_report = (f"Current Temperature: {temperature} Kelvin, "
                              f"Humidity: {humidity}%, "
                              f"Wind Speed: {wind_speed} meter per second, "
                              f"Weather Description: {weather_desc}")
            print(weather_report)
            speak(weather_report)
        else:
            speak("City not found.")
    elif 'goodbye' in command:
        speak("Goodbye!")
        return True  
    else:
        speak("I'm not sure how to help with that.")
    return False

if __name__ == "__main__":
    speak("I'm ready for your command.")
    while True:
        command = listen()  
        if command:
            if process_command(command): 
                break