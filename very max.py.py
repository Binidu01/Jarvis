import pyttsx3
import pywhatkit
import speech_recognition as sr
import datetime
import sys
import wikipedia 
import webbrowser
from googlesearch import search
import os
import openai
import cv2
import smtplib
from email.message import EmailMessage


camera = cv2.VideoCapture(0)
def capture_image():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    camera.release()
    return frame


openai.api_key = "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"

def speak(audio):
    rate = 200
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        message = "Good Morning sir!"
    elif 12 <= hour < 16:
        message = "Good Afternoon sir!"
    elif 16 <= hour < 19:
        message = "Good Evening sir!"
    else:
        message = "Good Night sir!"
    speak(message)

    introduction = """
      how may I assist you today, sir!
    """
    speak(introduction)

def google_search(query, num_results=10):
    search_results = []
    count = 0

    for result in search(query, num_results=num_results):
        search_results.append(result)
        count += 1
        if count >= num_results:
            break

    return search_results

def get_website_url(query):
    search_results = list(search(query, num_results=1))
    if search_results:
        return search_results[0]
    return None

def open_website(text):
    website_url = get_website_url(text)
    if website_url:
        webbrowser.open(website_url)
    else:
        print("Website is not found,sir.")
        speak("Website is not found,sir.")

def search_and_open(query):
    query = query.replace("search", "").strip()
    google_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(google_url)

def shutdown():
    os.system("shutdown /s /t 10")

def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def restart():
    os.system("shutdown /r /t 10")

def perform_actions(text):
    text_lower = text.lower()  

    if any(keyword in text_lower for keyword in ['wikipedia', 'wiki']):
        speak('Searching Wikipedia...')
        query = text_lower.replace("wikipedia", "").replace("wiki", "")
        results = wikipedia.summary(query, sentences=5)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif any(keyword in text_lower for keyword in ['open youtube']):
        webbrowser.open("https://www.youtube.com")
        speak("opening youtube,sir")

    elif any(keyword in text_lower for keyword in ['open google']):
        webbrowser.open("https://www.google.com")
        speak("opening google,sir")

    elif any(keyword in text_lower for keyword in ['your name']):
        speak("I am jarvis,sir")

    elif any(keyword in text_lower for keyword in ['yt','youtube','white','whity']):
        query = text_lower.replace("play in youtube", "").replace("search in youtube", "").replace("search in yt", "").replace("play in yt", "").replace("play in white", "").replace("search in whity", "")
        speak('searching on youtube sir!')
        pywhatkit.playonyt(query)

    elif any(keyword in text_lower for keyword in ['music']):
        music_dir = r"E:\movies\VIBE" 
        songs = os.listdir(music_dir)
        speak("playing music,sir")
        print(songs)    
        os.startfile(os.path.join(music_dir, songs[0]))

    elif any(keyword in text_lower for keyword in ['time']):
        strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
        print(f"Sir, the current time is {strTime}")    
        speak(f"Sir, the current time is {strTime}")

    elif any(keyword in text_lower for keyword in ['open vs code']):
        speak("opening vs code,sir")
        codePath = r"C:\Users\User\AppData\Local\Programs\Microsoft VS Code\Code.exe" 
        os.startfile(codePath)
        
    elif any(keyword in text_lower for keyword in ['bye','good bye','goodbye']):
                    print("Goodbye!,sir")
                    speak("Goodbye!,sir")
                    sys.exit()

    elif any(keyword in text_lower for keyword in ['shutdown my pc','shut down my pc']):
                    print("your pc will shutdown in 10 seconds,sir")
                    speak("your pc will shutdown in 10 seconds,sir")
                    shutdown()

    elif any(keyword in text_lower for keyword in ['restart my pc']):
                    print("your pc will restart in 10 seconds,sir")
                    speak("your pc will restart in 10 seconds,sir")
                    restart()

    elif any(keyword in text_lower for keyword in ['sleep my pc']):
                    print("your pc is in sleeping mode,sir")
                    speak("your pc is in sleeping mode,sir")
                    sleep()

    elif any(keyword in text_lower for keyword in ['links','urls']):
        query = text_lower.replace("urls", "")
        results = google_search(query)
        speak("searching the URLs, sir")
        print("\nSearch Results:")
        for i, result in enumerate(results, start=1):
            print(f"{i}. {result}")
            speak(f"{i}. {result}")
            
    elif any(keyword in text_lower for keyword in ['open']):
        query = text_lower.replace("open", "")
        speak(f"opening{query}, sir")
        open_website(text)

    elif any(keyword in text_lower for keyword in ['search for', 'search']):
        query = text_lower.replace("search", "").replace("search for", "")
        speak(f"searching {query} in google,sir")
        search_and_open(query)
        
    elif any(keyword in text_lower for keyword in ['whatsapp message']):
        speak('OK sir, please provide the recipient\'s WhatsApp number (with country code) and the message.')
        target_number = input("Enter the recipient's WhatsApp number (with country code): ")
        message = input("Enter the message you want to send: ")
        speak('Thank you sir, Sending the message.')
        current_time = datetime.datetime.now()
        pywhatkit.sendwhatmsg(target_number, message, current_time.hour, current_time.minute + 1)

    elif any(keyword in text_lower for keyword in ['email','gmail','mail']):
        speak('OK sir, please provide the recipient\'s email address,subject and the message.')
        recipient_email = input("Enter the recipient's email address: ")
        email_subject = input("Enter the email subject: ")
        email_message = input("Enter the email message: ")
        message = EmailMessage()
        message.set_content(email_message)
        message['From'] = 'binidupavith25@gmail.com'
        message['To'] = recipient_email
        message['Subject'] = email_subject
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('binidupavith25@gmail.com', 'nshsijgxslbimmpw')
                server.send_message(message)
                print("Email sent successfully!,sir")
                speak("Email sent successfully!,sir")
        except Exception as e:
            print("An error occurred sir:", e)
            speak("An error occurred sir:", e)
            

    elif any(keyword in text_lower for keyword in ['image']):
        image = capture_image()
        speak("Capturing your image, sir.")
        image = capture_image()
        cv2.imshow("Captured Image", image)
        speak("the image will be closed in 10 seconds, sir.")
        cv2.waitKey(10000)
        cv2.destroyAllWindows()
        speak("Window closed after 10 seconds.")

    return any(keyword in text_lower for keyword in ['wikipedia','email','gmail','mail','whatsapp message','image','open','wiki','urls','links', 'youtube','yt','search','white','your name','sleep my pc','shutdown my pc','shut down my pc','restart my pc', 'google', 'music', 'time', 'vs code','goodbye'])

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

def main():
    wishMe()

    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                print("Listening...")
                audio = r.listen(source)
                text = r.recognize_google(audio)
                print(f"User said: {text}\n")
                
                if not perform_actions(text):
                    messages = [{"role": "user", "content": text}]
                    response = send_to_chatGPT(messages)
                    print(response)
                    speak(response)

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

if __name__ == "__main__":
    main()
