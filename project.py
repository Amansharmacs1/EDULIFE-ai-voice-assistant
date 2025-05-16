import eel
import os
import webbrowser
from feature import (takecommand, speak, play_music, next_song, open_website, 
                    change_voice, send_whatsapp_message, chatBot, play_youtube,
                    shutdown_system, restart_system, call_person, reboot_device,
                    check_storage, toggle_bluetooth, check_battery_status,
                    take_screenshot, toggle_wifi, set_health_reminder, open_app_by_name,
                    calculate_bmi, introduce_assistant, get_numeric_input)    

# Initialize eel with your web files directory
print("Current working directory:", os.getcwd())
eel.init('front')   

@eel.expose 
def test_connection():
    print("Test function called from JavaScript!")
    return {"status": "success", "message": "Python connection working!"}

@eel.expose
def initialize_assistant():
    try:    
        print("Initializing voice assistant...")
        speak("Hello, I am your voice assistant. What can I do for you?")
        return {"status": "success", "message": "Assistant initialized"}
    except Exception as e:
        print(f"Error initializing assistant: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def start_jarvis():
    try:
        print("Starting Jarvis...")
        # Get the voice command
        print("Listening for command...")
        query = takecommand()
        print(f"Received command: {query}")
        
        if query and query.lower() != 'none':
            # Process the command
            print("Processing command...")
            result = process_command(query.lower())
            
            # Handle different response formats
            if isinstance(result, dict):
                response = {
                    "status": "success",
                    "query": query,
                    "response": result.get('message', ''),
                    "is_code": result.get('is_code', False),
                    "code_language": result.get('code_language', 'plaintext'),
                    "is_chatbot": result.get('is_chatbot', False),
                    "full_response": result.get('full_response', result.get('message', ''))
                }
            else:
                response = {
                    "status": "success",
                    "query": query,
                    "response": str(result),
                    "is_code": False,
                    "is_chatbot": False,
                    "full_response": str(result)
                }
            
            # Show speaking status and speak response only if not flagged to skip
            print("Speaking response...")
            if not (isinstance(result, dict) and result.get('skip_speak', False)):
                speak(response['response'])
            
            return response
        else:
            print("No command detected or command was 'None'")
            return {"status": "listening", "message": "Waiting for command..."}
            
    except Exception as e:
        print(f"Error in start_jarvis: {e}")
        return {"status": "error", "message": str(e)}

def process_command(query):
    try:
        print(f"Processing command: {query}")
        eel.showThinking()()  # Show thinking status while processing

        # Introduction command - Add this before other conditions
        if any(phrase in query for phrase in ["who are you", "introduce yourself", "what is your name", "tell me about yourself"]):
            print("Introduction requested")
            result = introduce_assistant()
            return {
                **result,
                "skip_speak": True  # Add flag to skip speaking again
            }

        # BMI calculation - Move this before other conditions
        if any(phrase in query for phrase in ["calculate bmi", "check bmi", "body mass index", "calculate my bmi", "what is my bmi", "find my bmi"]):
            print("BMI calculation requested")
            return calculate_bmi()

        # YouTube and music commands
        if "play" in query:
            # First check for YouTube specific commands
            if "on youtube" in query or "youtube" in query:
                print(f"YouTube command detected: {query}")
                return play_youtube(query)
            # Then check for music specific commands
            elif "music" in query:
                song_name = query.replace("play music", "").strip()
                print(f"Playing music: {song_name if song_name else 'default'}")
                return play_music(song_name if song_name else None)
            # Finally, treat as a general play command
            else:
                song_name = query.replace("play", "").strip()
                print(f"Playing song: {song_name}")
                # Try YouTube first for better song availability
                return play_youtube(f"{song_name} song")
        elif "next song" in query:
            return next_song()
        
        # Website and app handling
        elif "open" in query:
            # Check for device-specific commands
            if "on device" in query or "on my device" in query or "on mobile" in query or "app" in query:
                app_name = query.replace("open", "").replace("on device", "").replace("on my device", "").replace("on mobile", "").replace("app", "").strip()
                print(f"Opening app on device: {app_name}")
                
                # Use the open_app_by_name function to open the app
                success = open_app_by_name(app_name)
                if success:
                    return {
                        "status": "success",
                        "message": f"Opening {app_name} on your device",
                        "full_response": f"I am opening {app_name} on your mobile device using ADB."
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Could not open {app_name} on your device",
                        "full_response": f"I was unable to open {app_name} on your device. Please make sure your device is connected via USB and USB debugging is enabled."
                    }
            else:
                # Handle website opening
                print(f"Opening website: {query}")
                result = open_website(query)
                return {
                    "status": "success",
                    "message": "Website opened successfully",
                    "full_response": f"I've opened the website in your browser."
                } if result else {
                    "status": "error",
                    "message": "Website not found",
                    "full_response": "I couldn't find or open that website. Please check the URL and try again."
                }
        
        # Voice changes
        elif "change voice" in query:
            return change_voice()
        
        # WhatsApp messaging
        elif any(phrase in query for phrase in ["send message", "send whatsapp", "whatsapp message"]):
            print(f"WhatsApp command detected: {query}")
            
            # Extract contact if provided in the command
            contact = None
            if "to" in query:
                contact = query.split("to")[-1].strip()
            
            if not contact:
                speak("Who should I send the message to?")
                contact = takecommand()
                
            if contact and contact.lower() != 'none':
                print(f"Contact identified: {contact}")
                speak("What message should I send?")
                message = takecommand()
                
                if message and message.lower() != 'none':
                    print(f"Message received: {message}")
                    result = send_whatsapp_message(contact, message)
                    return {
                        "status": result.get("status", "error"),
                        "message": result.get("message", "Message sent"),
                        "full_response": f"Message sent to {contact}: '{message}'"
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Could not understand message",
                        "full_response": "I couldn't understand the message content. Please try again."
                    }
            else:
                return {
                    "status": "error",
                    "message": "Could not understand contact",
                    "full_response": "I couldn't understand the contact name. Please try again."
                }
        
        # System controls
        elif "shutdown" in query or "shut down" in query:
            return shutdown_system()
        elif "restart" in query:
            return restart_system()
        elif "reboot device" in query:
            return reboot_device()
        
        # System checks
        elif "check storage" in query:
            return check_storage()
        elif "battery status" in query or "check battery" in query:
            return check_battery_status()
        elif "take screenshot" in query:
            return take_screenshot()
        
        # Connectivity controls
        elif "bluetooth" in query:
            state = "on" if "on" in query else "off"
            return toggle_bluetooth(state)
        elif "wifi" in query or "wi-fi" in query:
            state = "on" if "on" in query else "off"
            return toggle_wifi(state)
        
        # Health reminders
        elif "set reminder" in query or "remind me" in query:
            if "water" in query:
                speak("How often (in minutes) would you like me to remind you to drink water?")
                minutes = get_numeric_input()
                return set_health_reminder("drink water", minutes)
            elif "break" in query:
                speak("How often (in minutes) would you like me to remind you to take a break?")
                minutes = get_numeric_input()
                return set_health_reminder("take break", minutes)
            elif "exercise" in query:
                speak("How often (in minutes) would you like me to remind you to exercise?")
                minutes = get_numeric_input()
                return set_health_reminder("exercise", minutes)
            elif "meal" in query or "eat" in query:
                speak("How often (in minutes) would you like me to remind you to eat?")
                minutes = get_numeric_input()
                return set_health_reminder("eat", minutes)
            
        # Time query
        elif "what time" in query or "tell time" in query:
            import datetime
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
            return {
                "status": "success", 
                "message": f"Current time: {current_time}",
                "full_response": f"The current time is {current_time}"
            }
            
        # Call handling
        elif "call" in query:
            name = query.replace("call", "").strip()
            if name:
                return call_person(name)
            else:
                return {
                    "status": "error", 
                    "message": "No name provided for call",
                    "full_response": "I need a name to make the call. Who would you like to call?"
                }
        
        # Default to chatbot for other queries
        else:
            print("\n=== Processing Chatbot Query ===")
            print(f"Query: {query}")
            
            result = chatBot(query)
            print("\n=== Chatbot Result ===")
            print(result)
            
            if result.get('status') == 'success':
                response_text = result.get('full_response', '')
                print("\n=== Response Text Being Sent to UI ===")
                print(response_text)
                
                return {
                    "status": "success",
                    "message": "Chatbot response received",
                    "response": response_text,
                    "is_chatbot": True,
                    "full_response": response_text,
                    "query": query
                }
            return {
                "status": "error",
                "message": result.get('message', 'Unknown chatbot error'),
                "is_chatbot": True,
                "full_response": result.get('message', 'I encountered an error while processing your request.'),
                "query": query
            }
            
    except Exception as e:
        error_msg = f"Error processing command: {e}"
        print(error_msg)
        speak("Sorry, I encountered an error with that command")
        eel.hideInterface()()  # Hide interface on error
        return {
            "status": "error", 
            "message": error_msg,
            "full_response": "I apologize, but I encountered an error while processing your command. Please try again."
        }

@eel.expose
def process_text_input(message):
    try:
        print(f"Processing text input: {message}")
        # Process the command
        result = process_command(message.lower())
        
        # Handle different response formats
        if isinstance(result, dict):
            response = {
                "status": "success",
                "response": result.get('message', ''),
                "is_code": result.get('is_code', False),
                "code_language": result.get('code_language', 'plaintext'),
                "is_chatbot": result.get('is_chatbot', False),
                "full_response": result.get('full_response', result.get('message', ''))
            }
        else:
            response = {
                "status": "success",
                "response": str(result),
                "is_code": False,
                "is_chatbot": False,
                "full_response": str(result)
            }
        
        return response
        
    except Exception as e:
        print(f"Error processing text input: {e}")
        return {
            "status": "error",
            "message": str(e),
            "full_response": f"I apologize, but I encountered an error: {str(e)}"
        }

# Start the application
if __name__ == "__main__":
    try:
        print("Starting voice assistant application...") 
        speak("Voice assistant is ready")
        
        # Try different ports if 8000 is unavailable
        port = 8000
        while port < 8010:  # Try ports 8000-8009
            try:
                print(f"Attempting to start server on port {port}...")
                # Start with index.html, allow any available browser
                eel.start('index.html', mode='default', port=port, host='localhost')
                break
            except Exception as e:
                if "Couldn't find chrome" in str(e):
                    # If Chrome is not available, try with the default browser
                    print("Chrome not found, trying with default browser...")
                    eel.start('index.html', mode='default', port=port, host='localhost')
                    break
                elif "Access is denied" in str(e) or "already in use" in str(e):
                    print(f"Port {port} is in use, trying next port...")
                    port += 1
                else:
                    raise e
        else:
            print("Could not find an available port between 8000-8009")
            speak("Error starting the application - all ports are busy")
            
    except Exception as e:
        print(f"Error starting application: {e}")
        speak("Error starting the application")
        # Wait for user input before closing
        input("Press Enter to exit...")
