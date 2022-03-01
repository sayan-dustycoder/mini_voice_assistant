import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import os
import pywhatkit as kit
import smtplib
import requests
from bs4 import BeautifulSoup


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')  # getting details of current voice
engine.setProperty('voice', voice[0].id)


if __name__ == "__main__":
    speak("Welcome to C M R I T")


def wishMe():
    hour = int(datetime.datetime.now().hour)
    user = takeUserName()
    if 00 >= hour > 12:
        speak(f"Good Morning {user}")
    elif 12 <= hour < 16:
        speak(f"Good afternoon {user}")
    else:
        speak(f"Good evening {user}")

    speak(f"What can I do for you {user}")

def takeUserName():
    speak("What shall I call you, sir or ma'am")
    user = takeCommand()

    return user


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        q = r.recognize_google(audio, language='en-in')  # Using google for voice recognition.
        print(f"User said: {q}\n")  # User query will be printed.

    except Exception as e:
        print(e)
        print("Say that again please...")  # Say that again will be printed in case of improper voice
        return "None"  # None string will be returned
    return q


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sayan0990basu@gmail.com', 'xyz')
    server.sendmail('sayan0990basu@gmail.com', to, content)
    server.close()


def covidCases():
    url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'

    # get URL html
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    data = []

    # soup.find_all('td') will scrape every
    # element in the url's table
    data_iterator = iter(soup.find_all('td'))

    # data_iterator is the iterator of the table
    # This loop will keep repeating till there is
    # data available in the iterator
    while True:
        try:
            country = next(data_iterator).text
            confirmed = next(data_iterator).text
            deaths = next(data_iterator).text
            continent = next(data_iterator).text

            data.append((
                country,
                int(confirmed.replace(',', '')),
                int(deaths.replace(',', '')),
                continent
            ))

        # StopIteration error is raised when
        # there are no more elements left to
        # iterate through
        except StopIteration:
            break

    # Sort the data by the number of confirmed cases
    data.sort(key=lambda row: row[1], reverse=True)
    return data


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()  # Converting user query into lower case

        # Logic for executing tasks based on query
        if query == "None":
            continue

        elif 'wikipedia' in query:  # if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'play on youtube' in query:
            speak("What should I play")
            vid = takeCommand()
            speak(f"Playing {vid} on youtube")
            kit.playonyt(vid)

        elif 'google' in query:
            query = query.replace("google", "")
            speak(f"Searching {query} on google")
            kit.search(query)

        elif 'whats app' in query:
            speak("Please say the number")
            number = takeCommand()
            speak("Please say the content to send")
            content = takeCommand()
            kit.sendwhatmsg_instantly(number, content)

        elif 'play music' in query:
            music_dir = 'C:\\Users\\DELL\\Music\\Playlists'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code editor' in query:
            codePath = r"C:\Users\DELL\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code"
            os.startfile(codePath)

        elif 'open terminal' in query:
            codePath = r'C:\Users\DELL\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\System Tools' \
                       r'\Command Prompt.lnk'
            os.startfile(codePath)

        elif 'open discord' in query:
            codePath = r"C:\Users\DELL\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc"
            os.startfile(codePath)

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "rijuthmenon@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend, I am not able to send this email")

        elif 'covid data' in query:
            speak("Which country's covid data would you like to get an info on")
            country = takeCommand()
            data = covidCases()
            if "all" in country:
                for case in data:
                    for section in case:
                        speak(str(section))
            else:
                for case in data:
                    if country in case[0]:
                        for section in case:
                            speak(str(section))

        elif "shutdown" in query:
            os.system("shutdown /s /t 1")
