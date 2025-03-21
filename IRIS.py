import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import os
import webbrowser
import subprocess
import requests
import random

# Initialize Text-to-Speech
engine = pyttsx3.init()

def set_voice():
    """Set the assistant voice."""
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Use the second voice (usually female)
    engine.setProperty("rate", 190)  # Speech speed
    engine.setProperty("volume", 1.0)  # Maximum volume

def speak(text):
    """Convert text to speech and print output."""
    print(f"Iris: {text}")
    engine.say(text)
    engine.runAndWait()

set_voice()

def recognize_speech():
    """Capture and recognize speech from microphone with improved accuracy."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Im Listening Jessie... Speak now!")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)  # Reduce background noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Capture audio
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError:
            speak("Speech recognition service unavailable.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def get_time():
    """Return the current time."""
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {now}."

def get_date():
    """Return the current date."""
    today = datetime.datetime.today().strftime("%B %d, %Y")
    return f"Today's date is {today}."

def open_application(app_name):
    """Open common applications like Notepad, Calculator, Browsers."""
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "file explorer": "explorer.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    }
    
    app_name = app_name.lower()
    if app_name in apps:
        try:
            subprocess.Popen(apps[app_name], shell=True)
            return f"Opening {app_name}..."
        except Exception as e:
            return f"Failed to open {app_name}: {e}"
    else:
        return f"Sorry, I can't open {app_name}."

def open_website(site_name):
    """Open common websites using web browser."""
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "chatgpt": "https://chat.openai.com",
        "github": "https://github.com",
        "linkedin": "https://www.linkedin.com",
        "gemini": "https://gemini.google.com",
        "gmail": "https://mail.google.com/mail/u/1/#inbox"
    }
    
    site_name = site_name.lower()
    if site_name in sites:
        try:
            webbrowser.open(sites[site_name])
            return f"Opening {site_name}..."
        except Exception as e:
            return f"Failed to open {site_name}: {e}"
    else:
        return "I can't find that website."

def search_wikipedia(query):
    """Fetch Wikipedia summary."""
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Please be more specific: {e.options[:3]}"
    except wikipedia.exceptions.PageError:
        return "No matching results found on Wikipedia."
    except Exception as e:
        return f"An error occurred: {e}"

def tell_joke():
    """Tell a random joke."""
    jokes = [
        "Why don't skeletons fight each other? Because they don't have the guts!",
        "Why was the math book sad? Because it had too many problems.",
        "I told my computer I needed a break, and now it won’t stop sending me vacation ads!"
    ]
    return random.choice(jokes)

def process_command(command):
    """Process user voice commands and execute appropriate tasks."""
    if not command:
        return None

    command = command.lower().strip()

    if "hello" in command or "hi" in command:
        return "Hello Jessie! I'm IRIS!! How can I assist you?"
    elif "how are you" in command:
        return "I'm Completely fine, What 'bout you?!"
    elif "I'm fine " in command:
        return "Great to hear!! So, how may I assist you?"
    elif "time" in command:
        return get_time()
    elif "date" in command:
        return get_date()
    elif "open" in command:
        app_name = command.replace("open", "").strip()
        return open_application(app_name)
    elif "go to" in command:
        site_name = command.replace("go to", "").strip()
        return open_website(site_name)
    elif "search" in command:
        query = command.replace("search", "").strip()
        return search_wikipedia(query)
    elif "joke" in command:
        return tell_joke()
    elif "exit" in command or "stop" in command:
        speak("Looking forward to help you again ! Have a great time!")
        exit(0)
    else:
        return "I'm not sure how to respond to that."

def main():
    """Main function to run the voice assistant."""
    speak("Say 'Iris' to activate.")

    while True:
        print("\nWaiting for activation...")
        activation_command = recognize_speech()

        if activation_command and "iris" in activation_command:
            speak(" Oh hey, Im IRIS!! how can I help you ...")

            while True:
                print("\n Im Waiting for your command...")
                command = recognize_speech()
                
                if command:
                    print(f" Kay working on it: {command}")  # Debugging output
                    response = process_command(command)

                    if response:
                        speak(response)
                    
                    if "exit" in command or "stop" in command:
                        speak("Looking forward to help you again ! Have a great time!")
                        return  # Exit assistant
                else:
                    print(" So You woke up for no reason, Don't disturb for no reason!! I'm sleeping ...")
                    break  # Go back to waiting for 'Iris'

if __name__ == "__main__":
    main()
