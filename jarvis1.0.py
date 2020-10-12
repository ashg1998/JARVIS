import pyttsx3
import datetime
import speech_recognition  as sr
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import time
import pyautogui
import json
import requests
import random
import os
from urllib.request import urlopen
import wolframalpha
import time
from quoters import Quote


engine = pyttsx3.init()
 


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time = datetime.datetime.now().strftime("%I:%M%S")#for 24 hour
    speak("The  current time is")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day
    speak("the current date is")
    speak(date)
    speak(month)
    speak(year)

def wishme():
    speak("welcome back Ashish!")
    time_()
    date_()
    #Greetings

    hour = datetime.datetime.now().hour
    if hour >=6 and hour<12:
        speak("Good Morning Sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    elif hour>=18 and hour<24:
        speak("Good Evening Sir!")
    else:
        speak("Good Night")
    

    speak("Jarvis at your service,how can i help you")
    speak("Here is something interesting")
    speak(Quote.print())
    

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing")
        query = r.recognize_google(audio, language='en-US')
        print(query)
    
    except Exception as e:
        print(e)
        print("Sorry can't recognize")
        return "None"
    return query


def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('userid@gmail.com','password')
    server.sendmail('userid@gmail.com',to,content)
    server.close()

def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at+'+usage )

    battery = psutil.sensors_battery()
    speak('Battery is at')
    speak(battery)

def joke():
    speak(pyjokes.get_joke())

def screenshot():
    name = int(round(time.time()*1000))
    name = 'F://JARVIS//Screenshotdata{}.png'.format(name)
    time.sleep(5)
    img = pyautogui.screenshot(name)
    img.save(name)


if __name__ == "__main__":

    wishme()

    while True:
        query = TakeCommand().lower()

        #All commands will be stored in lower case in query
        #for easy recognition

        if 'time' in query : #tell us time when asked
            time_()
        
        elif 'date' in query:
            date_()

        elif 'wikipedia' in query:
            speak("Searching.....")
            query = query.replace('wikipedia','')
            result = wikipedia.summary(query,sentences = 3)
            speak('According to Wikipedia')
            print(result)
            speak(result)
        elif 'send mail' in query:
            try:
                speak("What should I say")
                content = TakeCommand()
                speak("who is the receiver?")
                receiver =input("Enter Receiver's email")
                
                to = receiver
                sendEmail(to,content)
                speak(content)
                speak('email is send')

            except Exception as e:
                print(e)
                speak("Unable to send Email.")

        elif 'search in chrome' in query:
            speak('What should i Search')
            chrome_path ='C://Program Files//Google//Chrome//Application//chrome.exe %s'

            search = TakeCommand().lower()
            url_given = search+'.com'
           
            wb.get(chrome_path).open(url_given)
        
        elif 'search youtube' in query:
            speak("What should I search")
            search_term = TakeCommand().lower()
            speak("Here we go to YouTube!")
            wb.open('https://www.youtube.com/result?search_query='+search_term)

        elif 'search google' in query:
            speak('what should I search')
            search_term = TakeCommand().lower()
            speak('Searching.....')
            wb.open('https://www.google.com/search?q='+search_term)
        
        elif 'cpu' in query:
            cpu()
        
        elif 'joke' in query:
            joke()

        elif 'go offline' in query:
            speak('Going Offline Sir!')        
            quit()
        
        elif 'write a note' in query:
            speak("What should I write , Sir?")
            notes = TakeCommand()
            file = open('notes.txt','w')
            speak("Sir should I include Date and Time")
            ans = TakeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(':-')
                file.write('Done Taking Notes, SIR!')
            else:
                file.write(notes)
        
        elif 'show notes' in query:
            speak('showing notes')
            file = open('notes.txt','r')
            print(file.read())
            speak(file.read())

        elif 'screenshot' in query:
            screenshot()
        
        elif 'play music' in query:
            songs_dir = 'E:/SONGS'
            music = os.listdir(songs_dir)
            speak('What should I play?')
            speak('select a number.....')
            ans = TakeCommand().lower()
            if 'number' in ans:
                no = int(ans.replace('number',''))
                os.startfile(os.path.join(songs_dir,music[no]))
            elif 'random' or 'you choose' in ans:
                no = random.randint(1,2)
                os.startfile(os.path.join(songs_dir,music[no]))
        
        elif 'remember that' in query:
            speak('What should I remember that')
            memory = TakeCommand()
            speak('You should me to remember that'+memory)
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()
        
        elif 'do you remember anything' in query:
            remember = open('memory.txt','r')
            speak('You asked me to remember that'+remember.read())
        
        elif 'news' in query:
            try:
                jsonObj = urlopen("http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=6afaa26dea13469993a60619bb804ba8")
                data = json.load(jsonObj)
                i=1
                speak("here are some top headlines from business in India ")
                print('====================TOP HEADLINES==========================')
                for item in data['articles']:
                    print(str(i)+' '+item['title']+'\n')
                    print(item['description']+'\n')
                    speak(item['title'])
                    i+=1
                
            except Exception as e:
                print(str(e))
        
        elif 'where is' in query:
            query = query.replace("where is","")
            locations = query
            speak('User asked to locate'+locations)
            wb.open_new_tab("https://www.google.com/maps/place/"+locations)


        elif 'calculate' in query:
            client = wolframalpha.Client('6PWXRJ-25KKYQG64T')
            index = query.lower().split().index('calculate')
            query = query.split()[index+1:]
            res = client.query(''.join(query))
            answer = next(res.results).text
            print('Answer is :'+answer)
            speak('Answer'+answer)
        
        elif 'what is' in query or 'who is' in query:
            client = wolframalpha.Client('6PWXRJ-25KKYQG64T')
            res = client.query(query)
            
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("No result")

        elif 'stop listening' in query:
            speak('Ok Sir  stop listening  commands')
            
            time.sleep(10)
            
        
        elif 'log out' in query:
            os.system('shutdown -1')
        
        elif 'restart' in query:
            speak('Are you sure do you want to restart the system')
            ans = TakeCommand().lower()
            if 'yes' in ans:
                os.system('shutdown /r /t 1')
            
        
        elif 'shutdown' in query:
            speak('Are you sure do you want to shutdown the system')
            ans = TakeCommand().lower()
            if 'yes' in ans:
                os.system('shutdown /s /t 1')
        




            










