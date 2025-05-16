import os
import re
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
import requests
import sys
from hugchat import hugchat
import pyautogui 
import time
from pathlib import Path
import pywhatkit
import pywhatkit as kit
import pyaudio 
import threading
import eel
import urllib.parse
import webbrowser
import schedule

# Initialize pyttsx3
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
current_voice_index = 1 
engine.setProperty('voice', voices[current_voice_index].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to listen for commands
@eel.expose 
def takecommand():
    print("✅ takecommand() started")

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print('🎤 Listening...')
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            # Increase timeout and remove phrase time limit for better recognition
            r.pause_threshold = 0.8  # Reduced from 1 to make it more responsive
            r.energy_threshold = 4000  # Adjust if needed for your microphone
            print('👂 Ready for voice input...')
            audio = r.listen(source, timeout=None)  # Remove timeout for continuous listening
            
            print('🔍 Recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f'🗣 User said: {query}')
            return query.lower()
    except sr.WaitTimeoutError:
        print('⏰ Timeout: No speech detected.')
        return 'None'
    except sr.UnknownValueError: 
        print('❓ Could not understand audio.')
        return 'None'
    except sr.RequestError as e:
        print(f'🌐 Could not request results; {e}')
        return 'None'
    except Exception as e:
        print(f'❌ Other error: {e}')
        return 'None'

contacts = {
    "you": "919795542845",
    "ansh": "918957239463",
    "a": "919253203120",
    "harsh": "919625963078"
}

# Health reminder functions
def speak_reminder(message):
    speak(message)

def remind_to_drink_water():
    speak_reminder("It's time to drink water! Stay hydrated.")

def remind_to_take_break():
    speak_reminder("Take a break! Stretch your legs and relax for a few minutes.")

def remind_to_exercise():
    speak_reminder("Time for some exercise! Let's get moving.")

def remind_to_eat_meal():
    speak_reminder("It's time for your meal! Eat something healthy.")

def set_health_reminder(reminder_type, interval_minutes):
    if reminder_type == "drink water":
        schedule.every(interval_minutes).minutes.do(remind_to_drink_water)
    elif reminder_type == "take break":
        schedule.every(interval_minutes).minutes.do(remind_to_take_break)
    elif reminder_type == "exercise":
        schedule.every(interval_minutes).minutes.do(remind_to_exercise)
    elif reminder_type == "eat":
        schedule.every(interval_minutes).minutes.do(remind_to_eat_meal)
    else:
        speak("Sorry, I don't recognize that reminder type.")

    speak(f"Reminder set for {reminder_type} every {interval_minutes} minutes.")

def health_reminder_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the scheduler in a separate thread
threading.Thread(target=health_reminder_scheduler, daemon=True).start()

# Function to play music
def play_music(song_name=None):
    global current_song
    music_dir = "C:\\Users\\AMAN SINGH\\musicdirectory"
    try:
        if not os.path.exists(music_dir):
            speak("The specified music directory does not exist.")
            return
        songs = os.listdir(music_dir)
        music_files = [song for song in songs if song.endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a'))]
        if music_files:
            if song_name:
                song_name = song_name.lower()
                song_to_play = next((song for song in music_files if song_name in song.lower()), None)
                if song_to_play:
                    os.startfile(os.path.join(music_dir, song_to_play))
                    current_song = song_to_play
                    speak(f"Playing {song_to_play}.")
                else:
                    speak(f"Sorry, I couldn't find a song named {song_name}.")
            else:
                os.startfile(os.path.join(music_dir, music_files[0]))
                current_song = music_files[0]
                speak("Playing music.")
        else:
            speak("No music files found in the directory.")
    except Exception as e:
        print(e)
        speak("Sorry, I could not play music.")

# Function to play the next song
def next_song():
    global current_song
    music_dir = "C:\\Users\\AMAN SINGH\\musicdirectory"
    try:
        songs = os.listdir(music_dir)
        music_files = [song for song in songs if song.endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a'))]
        if music_files:
            if current_song:
                current_index = music_files.index(current_song)
                next_song = music_files[(current_index + 1) % len(music_files)]
            else:
                next_song = music_files[0]
            os.startfile(os.path.join(music_dir, next_song))
            current_song = next_song
            speak(f"Playing next song: {next_song}")
        else:
            speak("No music files found in the directory.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't play the next song.")

# Websites dictionary for opening websites
websites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "wikipedia": "https://www.wikipedia.org",
    "amazon": "https://www.amazon.com",    
    "netflix": "https://www.netflix.com",
    "reddit": "https://www.reddit.com",
    "github": "https://www.github.com",
    "stack overflow": "https://www.stackoverflow.com",
    "gmail": "https://mail.google.com",
    "outlook": "https://outlook.live.com",
    "whatsapp": "https://web.whatsapp.com",
    "bbc news": "https://www.bbc.com/news",
    "cnn": "https://www.cnn.com",
    "espn": "https://www.espn.com",
    "spotify": "https://www.spotify.com",
    "discord": "https://www.discord.com"
}
def open_app_by_name(app_name):
    apps = {
        "whatsapp": "com.whatsapp",  # Changed back to regular WhatsApp
        "youtube": "com.google.android.youtube",
        "facebook": "com.facebook.katana",
        "instagram": "com.instagram.android",
        "gmail": "com.google.android.gm",
        "chrome": "com.android.chrome",
        "google": "com.google.android.googlequicksearchbox",
        "maps": "com.google.android.apps.maps",
        "settings": "com.android.settings",
        "camera": "com.android.camera",
        "gallery": "com.android.gallery3d",
        "spotify": "com.spotify.music",
        "phone": "com.android.dialer",
        "messages": "com.android.mms",
        "calculator": "com.android.calculator2",
        "clock": "com.android.deskclock",
        "calendar": "com.android.calendar"
    }

    print(f"Attempting to open app: {app_name}")  # Debug print
    app_name = app_name.lower().strip()
    package = apps.get(app_name)
    
    if not package:
        print(f"Package not found for app: {app_name}")  # Debug print
        speak(f"Sorry, I couldn't find the app named {app_name} in my list of supported apps.")
        return False

    try:
        # Check ADB connection
        print("Checking ADB connection...")  # Debug print
        result = os.popen('adb devices').read()
        print(f"ADB devices result: {result}")  # Debug print
        
        if 'device' not in result:
            print("No device connected via ADB")  # Debug print
            speak("No Android device connected. Please connect your device and enable USB debugging.")
            return False
        
        # Try multiple methods to open the app
        print(f"Attempting to open package: {package}")  # Debug print
        
        # Method 1: Using monkey
        print("Trying monkey command...")  # Debug print
        os.system(f'adb shell monkey -p {package} -c android.intent.category.LAUNCHER 1')
        
        # Method 2: Using am start
        print("Trying am start command...")  # Debug print
        os.system(f'adb shell am start -n {package}/.MainActivity')
        
        # Method 3: Using am start without specific activity
        print("Trying generic am start command...")  # Debug print
        os.system(f'adb shell am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n {package}/.MainActivity')
        
        speak(f"Opening {app_name} on your device.")
        return True
        
    except Exception as e:
        print(f"Error opening app: {str(e)}")  # Debug print
        speak("Sorry, I encountered an error while trying to open the app.")
        return False

# Function to open websites
def open_website(query):
    for site, url in websites.items():
        if site in query:
            webbrowser.open(url)
            speak(f"Opening {site}.")
            return True
    return False

# Function to change voice
def change_voice():
    global current_voice_index  
    if current_voice_index == 0:
        current_voice_index = 1
        engine.setProperty('voice', voices[1].id)
        speak("Switching to female voice.")
    else:
        current_voice_index = 0
        engine.setProperty('voice', voices[0].id)
        speak("Switching to male voice.")

# Function to send WhatsApp messages
def send_whatsapp_message(contact, message):
    try:
        # Check if the contact is in our contacts dictionary
        contact_number = contacts.get(contact.lower())
        
        if not contact_number:
            # If not in contacts, clean and format the number
            contact_number = ''.join(filter(str.isdigit, contact))
            
        # Ensure number starts with country code
        if len(contact_number) == 10:
            contact_number = "91" + contact_number
        elif not (contact_number.startswith("91") or contact_number.startswith("+91")):
            speak("Please provide a valid Indian phone number")
            return {"status": "error", "message": "Invalid phone number format"}
            
        print(f"Formatted number: {contact_number}")  # Debug log
        
        # Remove any existing "+" and add it back
        contact_number = contact_number.replace("+", "")
        formatted_number = "+" + contact_number
        
        print(f"Sending message: {message} to {formatted_number}")  # Debug log
        
        # Increase wait time and add tab close
        kit.sendwhatmsg_instantly(
            formatted_number, 
            message,
            wait_time=20,  # Increased wait time
            tab_close=True  # Automatically close tab after sending
        )
        
        # Add a small delay to ensure the message is sent
        time.sleep(2)
        
        speak(f"Message sent to {contact}")
        return {"status": "success", "message": f"Message sent to {contact}"}
        
    except Exception as e:
        error_msg = f"Error sending WhatsApp message: {str(e)}"
        print(error_msg)  # Debug print
        
        # More specific error messages
        if "failed to establish a new connection" in str(e).lower():
            speak("Please check your internet connection")
            return {"status": "error", "message": "Internet connection error"}
        elif "chrome not found" in str(e).lower():
            speak("Please make sure Chrome browser is installed")
            return {"status": "error", "message": "Chrome browser not found"}
        elif "whatsapp web not found" in str(e).lower():
            speak("Please make sure you're logged into WhatsApp Web")
            return {"status": "error", "message": "WhatsApp Web not accessible"}
        else:
            speak("Sorry, I couldn't send the WhatsApp message")
            return {"status": "error", "message": error_msg}

# Function to interact with chatbot
def chatBot(query):
    try:
        user_input = query.lower()
        chatbot = hugchat.ChatBot(cookie_path="cookies.JSON.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        
        # Get the full response
        response = chatbot.chat(user_input)
        response_text = str(response)  # Convert response to string
        
        # Print for debugging
        print("\n=== Full Chatbot Response ===")
        print(f"Type: {type(response)}")
        print(f"Raw response: {response}")
        print(f"String response: {response_text}")
        print("===========================\n")

        # Extract first sentence for speaking
        # Split by common sentence endings and take the first part
        sentence_endings = ['. ', '? ', '! ']
        first_sentence = response_text
        for ending in sentence_endings:
            if ending in response_text:
                first_sentence = response_text.split(ending)[0] + ending.strip()
                break
        
        # Ensure the sentence isn't too long
        if len(first_sentence) > 150:
            first_sentence = first_sentence[:150] + "..."

        print(f"Speaking sentence: {first_sentence}")  # Debug print
        
        # First announce that response is received
        speak("Chatbot response received.")
        # Then speak the actual response
        speak(first_sentence)

        # Return the complete response
        return {
            "status": "success",
            "message": response_text,  # Use full text as message for display
            "full_response": response_text,  # Full text for display
            "type": "chatbot",
            "skip_speak": True  # Skip speaking in main loop since we already spoke
        }

    except Exception as e:
        error_msg = f"Chatbot error: {str(e)}"
        print(f"\n=== Chatbot Error ===\n{error_msg}\n==================\n")
        speak("Sorry, I could not get a response from the chatbot.")
        return {
            "status": "error",
            "message": error_msg,
            "type": "chatbot"
        }

# Function to play YouTube
def play_youtube(query):
    try:
        # Clean up the search query
        search_query = query.lower()
        print(f"Original query: {search_query}")  # Debug log
        
        # Remove common phrases
        for phrase in ["play", "on youtube", "youtube", "video"]:
            search_query = search_query.replace(phrase, "")
        search_query = search_query.strip()
        
        print(f"Cleaned search query: {search_query}")  # Debug log
        speak(f"Playing {search_query} on YouTube")
        
        # Use pywhatkit to play the video
        print(f"Calling pywhatkit.playonyt with query: {search_query}")  # Debug log
        pywhatkit.playonyt(search_query)
        return {"status": "success", "message": f"Playing {search_query} on YouTube"}
    except Exception as e:
        error_msg = f"Error playing YouTube video: {str(e)}"
        print(error_msg)  # Debug print
        speak("Sorry, I couldn't play that video on YouTube")
        return {"status": "error", "message": error_msg}

# System shutdown and restart functions
import platform
import os

def shutdown_system():
    speak("Shutting down the system now.")
    if platform.system() == "Windows":
        os.system("shutdown /s /t 5")
    elif platform.system() == "Linux":
        os.system("shutdown now")
    elif platform.system() == "Darwin":  # macOS
        os.system("sudo shutdown -h now")
    else:
        speak("Shutdown is not supported on this system.")

def restart_system():
    speak("Restarting the system now.")
    if platform.system() == "Windows":
        os.system("shutdown /r /t 5")
    elif platform.system() == "Linux":
        os.system("reboot")
    elif platform.system() == "Darwin":  # macOS
        os.system("sudo shutdown -r now")
    else:
        speak("Restart is not supported on this system.")
        
        
def get_numeric_input(prompt="Please say the number of minutes."):
    speak(prompt)
    while True:
        response = takecommand()
        numbers = re.findall(r'\d+', response)
        if numbers:
            return int(numbers[0])
        else:
            speak("Sorry, I didn't catch a number. Please say it again.")
def dial_number(number):
    # Clean the number by removing spaces or dashes
    number = number.replace(" ", "").replace("-", "")
    # Run the ADB command to launch the dialer with the provided number
    command = f'adb shell am start -a android.intent.action.DIAL -d tel:{number}'
    os.system(command)
    
    
def call_person(query):
    # Try to find a contact by name
    contact_number = contacts.get(query.lower())
    
    if contact_number:
        # Call predefined contact
        speak(f"Calling {query} at {contact_number}")
        dial_number(contact_number)
    else:
        # Ask the user for a phone number if not a contact
        speak("I couldn't find that contact, please provide the phone number.")
        number = takecommand()
        number = ''.join(re.findall(r'\d+', number))  # Extract only digits
        if not number.startswith('+91'):  # Ensure it starts with country code
            number = '+91' + number
        speak(f"Calling {number}")
        dial_number(number)
import subprocess

def reboot_device():
    subprocess.run(["adb", "reboot"])


def check_storage():
    storage_info = os.popen("adb shell df -h").read()
    total_space = re.search(r"(/data)(\s+)(\d+)(\s+)(\d+)", storage_info)
    if total_space:
        speak(f"Total space: {total_space.group(3)}, Available space: {total_space.group(5)}.")
    else:
        speak("Unable to retrieve storage information.")
def toggle_bluetooth(state="on"):
    if state == "on":
        os.system("adb shell am start -a android.settings.BLUETOOTH_SETTINGS")
        speak("Turning on Bluetooth.")
    elif state == "off":
        os.system("adb shell am start -a android.settings.BLUETOOTH_SETTINGS")
        speak("Turning off Bluetooth.")
def check_battery_status():
    battery_status = os.popen('adb shell dumpsys battery').read()
    battery_level = re.search(r"level: (\d+)", battery_status)
    if battery_level:
        speak(f"Your battery is at {battery_level.group(1)} percent.")
    else:
        speak("Unable to retrieve battery status.")
def take_screenshot():
    # Get the user's Pictures directory dynamically
    pictures_path = Path.home() / "Pictures"
    pictures_path.mkdir(parents=True, exist_ok=True)  # Create if not exists
    
    # Build the screenshot filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = pictures_path / f"screenshot_{timestamp}.png"

    # Capture and pull the screenshot using ADB
    os.system("adb shell screencap -p /sdcard/screenshot.png")
    os.system(f'adb pull /sdcard/screenshot.png "{screenshot_path}"')

    speak(f"Screenshot saved at {screenshot_path}")
    print(f"Screenshot saved at {screenshot_path}")


def toggle_wifi(state="on"):
    if state == "on":
        os.system("adb shell am start -a android.settings.WIFI_SETTINGS")
        speak("Turning on WiFi.")
    elif state == "off":
        os.system("adb shell am start -a android.settings.WIFI_SETTINGS")
        # Use commands to toggle off WiFi if possible (if required)
        speak("Turning off WiFi.")

def get_numeric_value_from_voice(prompt):
    # Remove the speak() call from here since it will be done in calculate_bmi
    while True:
        response = takecommand()
        if response == 'none':
            speak("I didn't catch that. Please try again.")
            continue
        
        # Extract numbers from the response
        numbers = re.findall(r'\d+\.?\d*', response)
        if numbers:
            return float(numbers[0])
        else:
            speak("Please say a number clearly.")

def calculate_bmi():
    try:
        # Get height in meters
        speak("Please tell me your height in centimeters")
        height_cm = get_numeric_value_from_voice("What is your height in centimeters?")
        height_m = height_cm / 100  # Convert to meters
        
        # Get weight in kg
        speak("Please tell me your weight in kilograms")
        weight_kg = get_numeric_value_from_voice("What is your weight in kilograms?")
        
        # Calculate BMI
        bmi = weight_kg / (height_m * height_m)
        
        # Determine BMI category and get suggestions
        if bmi < 18.5:
            category = "underweight"
            suggestions = [
                "Consider increasing your caloric intake",
                "Include more protein-rich foods in your diet",
                "Consult with a nutritionist for a proper diet plan",
                "Start strength training exercises",
                "Eat more frequent, smaller meals throughout the day"
            ]
        elif bmi < 25:
            category = "normal weight"
            suggestions = [
                "Maintain your current healthy lifestyle",
                "Continue with regular exercise",
                "Eat a balanced diet",
                "Stay hydrated",
                "Get regular health check-ups"
            ]
        elif bmi < 30:
            category = "overweight"
            suggestions = [
                "Increase physical activity to at least 30 minutes daily",
                "Reduce intake of processed foods",
                "Monitor portion sizes",
                "Include more fruits and vegetables in your diet",
                "Consider consulting with a healthcare provider"
            ]
        else:
            category = "obese"
            suggestions = [
                "Consult with a healthcare provider for a personalized plan",
                "Start with low-impact exercises like walking or swimming",
                "Focus on portion control",
                "Keep a food diary to track intake",
                "Consider working with a registered dietitian"
            ]
        
        # Prepare response
        response = f"Your BMI is {bmi:.1f}, which falls in the {category} category. Here are some suggestions for you:\n"
        for suggestion in suggestions:
            response += f"• {suggestion}\n"
        
        # Speak the BMI result and category
        speak(f"Your BMI is {bmi:.1f}. You are in the {category} category. Here are some suggestions for you:")
        
        # Speak suggestions
        for suggestion in suggestions:
            speak(suggestion)
            
        return {
            "status": "success",
            "message": response,
            "full_response": response,
            "bmi": bmi,
            "category": category
        }
        
    except Exception as e:
        error_msg = f"Error calculating BMI: {str(e)}"
        speak("Sorry, I encountered an error while calculating your BMI")
        return {"status": "error", "message": error_msg}

def introduce_assistant():
    introduction = "Hello, I am Aduvo your personal AI voice assistant. You can also call me Jarvis. I was created by Aman Singh, Aman, Ansh, and Anurag to make your digital life smarter and easier."
    speak(introduction)
    return {
        "status": "success",
        "message": introduction,
        "full_response": introduction
    }

# Main execution loop
if __name__ == "__main__":
    current_song = None
    speak("Hello! I'm ready to assist you.")
    while True:
        query = takecommand()
        if query == "none":
            continue

        query = query.lower()

        # Introduction command - Add this before other conditions
        if any(phrase in query for phrase in ["who are you", "introduce yourself", "what is your name", "tell me about yourself"]):
            introduce_assistant()
            continue

        # BMI calculation - Add this before other conditions
        if any(phrase in query for phrase in ["calculate bmi", "check bmi", "body mass index", "calculate my bmi", "what is my bmi", "find my bmi"]):
            calculate_bmi()
            continue

        # Add the health reminder commands
        if 'remind me to drink water' in query:
            minutes = get_numeric_input("How often (in minutes) would you like me to remind you?")
            set_health_reminder("drink water", minutes)

        elif 'remind me to take a break' in query:
            minutes = get_numeric_input("How often (in minutes) would you like me to remind you?")
            set_health_reminder("take break", minutes)

        elif 'remind me to exercise' in query:
            minutes = get_numeric_input("How often (in minutes) would you like me to remind you?")
            set_health_reminder("exercise", minutes)

        elif 'remind me to eat' in query:
            minutes = get_numeric_input("How often (in minutes) would you like me to remind you?")                                       
            set_health_reminder("eat", minutes)

        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Open app or website
        elif 'open' in query:
            print(f"Processing open command: {query}")  # Debug print
            
            # First check if it's a device app command
            if any(phrase in query for phrase in ["on device", "on my device", "on mobile", "app"]):
                print("Detected device app command")  # Debug print
                app_name = query.replace("open", "")
                for phrase in ["on device", "on my device", "on mobile", "app"]:
                    app_name = app_name.replace(phrase, "")
                app_name = app_name.strip()
                print(f"Extracted app name: {app_name}")  # Debug print
                
                # Try to open the app
                if not open_app_by_name(app_name):
                    print(f"Failed to open app: {app_name}")  # Debug print
                    speak(f"Could not open {app_name} on your device. Please make sure your device is connected and the app is installed.")
            
            # Then check if it's a website
            else:
                print("Checking if it's a website command")  # Debug print
                if not open_website(query):
                    print("Not a website, trying as an app")  # Debug print
                    # If not a website, try as an app
                    app_name = query.replace("open", "").strip()
                    print(f"Trying to open as app: {app_name}")  # Debug print
                    if not open_app_by_name(app_name):
                        print(f"Failed to open as app or website: {query}")  # Debug print
                        speak("Sorry, I couldn't find that website or app.")

        elif 'play' in query and 'on youtube' in query:
            play_youtube(query)

        elif 'play music' in query:
            play_music()

        elif 'play' in query:
            song_name = query.replace("play", "").strip()
            play_music(song_name)

        elif 'next song' in query:
            if current_song:
                next_song()
            else:
                speak("No song is currently playing.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is {strTime}")

        elif 'change voice' in query:
            change_voice()

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye, Sir!")
            sys.exit()

        elif 'very good' in query or 'excellent' in query:
            speak("Thank you, sir") 

        elif 'how are you' in query:
            speak("I am excellent sir, what about you?")

        elif 'send message to' in query:
            matched_contact = None 

        elif 'shut down' in query or 'shutdown' in query:
            shutdown_system()

        elif 'restart' in query or 'reboot' in query:
            restart_system()

        elif 'call' in query:
            # Handle calling predefined contacts or number input
            name_or_number = query.replace("call", "").strip()
            if name_or_number:
                call_person(name_or_number)
            else:
                speak("Whom should I call?")

        elif 'reboot my device' in query:
            reboot_device()

        # Additional small features
        elif 'turn on wifi' in query:
            toggle_wifi("on")

        elif 'turn off wifi' in query:
            toggle_wifi("off")

        elif 'take screenshot' in query:
            take_screenshot()

        elif 'check battery status' in query: 
            check_battery_status()

        elif 'turn on bluetooth' in query:
            toggle_bluetooth("on")

        elif 'turn off bluetooth' in query:
            toggle_bluetooth("off")

        elif 'check storage' in query:
            check_storage()

        else:
            chatBot(query)
