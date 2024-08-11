import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pyjokes
import os
import openai
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import apikey

chatStr = ""

def chat(data1):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"diksha: {data1}\n sofia: "
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": chatStr}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response.choices[0].message["content"]
        speechtx(response_text)
        chatStr += f"{response_text}\n"
        return response_text
    except Exception as e:
        print(f"Error: {e}")
        speechtx("Sorry, I couldn't process that request.")
        return None

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response.choices[0].message["content"]
    except Exception as e:
        text += f"\nError: {e}"
    
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    
    filename = f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
    filename = filename.replace('/', '_').replace('\\', '_')  # Sanitize filename
    with open(filename, "w") as f:
        f.write(text)

def sptext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        print("Audio captured, recognizing...")
        try:
            data = recognizer.recognize_google(audio)
            print(data)
            return data
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def speechtx(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def send_email(subject, body, to_email, from_email, password):
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the body with the msg instance
    message.attach(MIMEText(body, 'plain'))

    try:
        # Create SMTP session for sending the mail
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail's SMTP server
        server.starttls()  # Enable security
        server.login(from_email, password)  # Log in to the server
        text = message.as_string()  # Convert the message to a string
        server.sendmail(from_email, to_email, text)  # Send the email
        server.quit()  # Quit the server
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    speechtx("Welcome, Alexa here...")
    speechtx("How may I help you?")

    while True:
        data1 = sptext()
        if data1 is not None:
            data1 = data1.lower()
            if "your name" in data1:
                name = "My name is Alexa"
                speechtx(name)

            elif "old are you" in data1:
                age = "I'm developed by Diksha Kulkarni on 22nd July 2024, so please calculate my age yourself"
                speechtx(age)

            elif 'time' in data1:
                current_time = datetime.datetime.now().strftime("%H:%M %p")
                speechtx(f"Mam, the time is {current_time}")

            elif "youtube" in data1:
                speechtx("Opening YouTube, mam...")
                webbrowser.open("https://www.youtube.com/")

            elif "open vs code" in data1:
                os.system("code")

            elif "joke" in data1:
                joke_1 = pyjokes.get_joke(language="en", category="neutral")
                print(joke_1)
                speechtx(joke_1)

            elif "whatsapp" in data1:
                speechtx("Opening WhatsApp Web...")
                webbrowser.open("https://web.whatsapp.com/")

            elif "instagram" in data1:
                speechtx("Opening Instagram Web...")
                webbrowser.open("https://www.instagram.com/")

            elif "using artificial intelligence" in data1:
                ai(prompt=data1)

            elif "reset chat" in data1:
                chatStr = ""

            elif "send email" in data1:
                subject = "Test Subject"
                body = "This is a test email body."
                to_email = "receiver@example.com"
                from_email = "dikshank867@gmail.com"
                password = "DikshaNK@678"  # Use a more secure method in practice
                send_email(subject, body, to_email, from_email, password)
                speechtx("Email sent successfully.")

            elif "exit" in data1:
                speechtx("Thank you")
                break
        else:
            print("chatting")
            chat(data1)
