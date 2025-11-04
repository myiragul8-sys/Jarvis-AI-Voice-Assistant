import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
# pip install pocketsphinx
recognizer =sr.Recognizer()
engine=pyttsx3.init()
newsapi="f4b9f16c3e2540de8dab61912dbbbff8"
def speak_old(text):
    engine.say(text) 
    engine.runAndWait() 
def speak(text):
     
    tts = gTTS(text)
    tts.save('temp.mp3')
    

# Initialize pygame mixer
    pygame.mixer.init()

# Load and play the MP3 file
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

# Keep the program running while the music is playing
    while pygame.mixer.music.get_busy():  # Returns True if music is playing
       pygame.time.Clock().tick(10)
       pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client=OpenAI(api_key="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")
    completion=client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role":"system","content":"you are virtual assistance named jarvis skilled in general tasks like alexa and google cloud"},
              {"role":"user","content":command}]
)
    return(completion.choices[0].message.content)

def processCommand(c): 
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower() : 
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # parse the JSON response
            data = r.json()
            # extract the articles
            articles=data.get('articles',[])
    
            #  print headlines
            for article in articles:
                speak(article['title'])
    else:
        # open ai handle the requests   
        output=aiProcess(c)
        speak(output)
                

if __name__=="__main__":
    speak("initializing jarvis.....")

    while True:
       
         # listen for wake word "jarvis"
        # obtain audio from the microphone
        r=sr.Recognizer()
        print("recognizing..")
        try:
            with sr.Microphone() as source:
               print("listening.....")
               audio = r.listen(source,timeout=5,phrase_time_limit=3)
               print("recognizing...")
        
            word=r.recognize_google(audio)
            if "jarvis" in word.lower():
                speak("ya")
                # listen for command
                with sr.Microphone() as source:
                    print("jarvis active")
                    audio = r.listen(source,timeout=5,phrase_time_limit=3)
                    command=r.recognize_google(audio)
                    print(command)
                    processCommand(command)
        

        
        except Exception as e:
            print("Error; {0}".format(e))

    