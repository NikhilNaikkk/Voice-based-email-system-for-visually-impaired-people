from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

import sys
import cv2
import face_recognition
import smtplib
import imaplib
import email
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage

class Pybot(BoxLayout) :

    def _init_(self, **kwargs) :
        super(Pybot, self)._init_(**kwargs)

    def talk(self, text) :
        engine = pyttsx3.init()
        rate = engine.getProperty("rate")
        engine.setProperty("rate", 140)
        engine.say(text)
        engine.runAndWait()

    def get_info(self) :
        listener = sr.Recognizer()
        try :
            with sr.Microphone() as source :
                self.talk('listening....')
                voice = listener.listen(source)
                info = listener.recognize_google(voice)
                self.talk(info)
                return info.lower()
        except :
            self.talk("sorry I didn't understand")

    def send_email(self, receiver, subject, message) :
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('pybott11@gmail.com', '01373842')
        email = EmailMessage()
        email['From'] = 'pybott11@gmail.com'
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(message)
        server.send_message(email)

    email_list = {
        'nikhil' : 'nikhilnaik769@gmail.com',
        'nick' : 'nikhilnnaik1999@gmail.com',
        'sanskriti' : 'sanskritinaik264@gmail.com',
        'gopura' : 'gopuraprabhu@gmail.com',
        'akash' : 'akashcb2014@gmail.com'
    }

    def get_email_info(self) :
        self.talk('To whom you want to send Email?')
        name = self.get_info()
        receiver = self.email_list[name]
        self.talk(receiver)
        self.talk('What is the subject of your Email?')
        subject = self.get_info()
        self.talk('What you want to text in your Email?')
        message = self.get_info()
        self.talk('Sending Email to')
        self.talk(receiver)
        self.talk('The subject is')
        self.talk(subject)
        self.talk('The message is')
        self.talk(message)
        self.talk('Should I send your Email?')
        send = self.get_info()
        if ('yes' in send) or ('yeah' in send) or ('ok' in send) or ('send' in send) or ('yes send' in send) or ('yeah send' in send) or ('ok send' in send) :
            self.send_email(receiver, subject, message)
            self.talk('Hey,Your Email is sent!')
            self.talk('Do you want to send more Email?')
            send_more = self.get_info()
            if ('yes' in send_more) or ('yeah' in send_more) or ('yes I want' in send_more) or ('yeah I want' in send_more) or ('I want' in send_more) :
                self.get_email_info()
            elif ('no' in send_more) or ("no don't want" in send_more) or ("don't want" in send_more) or ("I don't want" in send_more) :
                self.talk('okay')
                self.get_input()
            else :
                self.talk("Sorry I can't help you with that.")
                self.get_input()
        elif ('no' in send) or ("no don't send" in send) or ("don't send" in send) :
            self.talk('okay , your Email is not sent')
            self.get_input()
        else :
            self.talk("Sorry I can't help you with that.")
            self.get_input()

    def get_inbox(self) :
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('pybott11@gmail.com', '01373842')
        mail.select("inbox")
        _, search_data = mail.search(None, 'UNSEEN')
        for num in search_data[0].split() :
            email_data = {}
            _, data = mail.fetch(num, '(RFC822)')
            _, b = data[0]
            email_message = email.message_from_bytes(b)
            self.talk('you have new email')

            for header in ['subject', 'to', 'from', 'date'] :
                self.talk("Email{}: {}".format(header, email_message[header]))
                email_data[header] = email_message[header]
            for part in email_message.walk() :
                if part.get_content_type() == "text/plain" :
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()
                    self.talk("Message written in the email {}:".format(email_data['body']))

    def get_sent(self) :
        server = "imap.gmail.com"
        imap = imaplib.IMAP4_SSL(server)
        imap.login('pybott11@gmail.com', '01373842')
        res, messages = imap.select('"[Gmail]/Sent Mail"')
        messages = int(messages[0])
        n = 3
        self.talk('Three recent mails sent by you')
        for i in range(messages, messages - n, -1) :
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg :
                if isinstance(response, tuple) :
                    msg = email.message_from_bytes(response[1])
                    From = msg["From"]
                    To = msg["To"]
                    Date = msg["Date"]
                    Subject = msg["Subject"]
                    email_data = {}
                    for part in msg.walk() :
                        if part.get_content_type() == "text/plain" :
                            body = part.get_payload(decode=True)
                            email_data['body'] = body.decode()

                    self.talk("From {}: ".format(From))
                    self.talk("To {}: ".format(To))
                    self.talk("Date {}: ".format(Date))
                    self.talk("Subject {}: ".format(Subject))
                    self.talk("Message written in the email! {}: ".format(email_data['body']))

            self.talk("Do you want to read more sent mails?")
            sent_mail = self.get_info()
            if ('yes' in sent_mail) or ('ok' in sent_mail) or ('yeah' in sent_mail) or ('yes read' in sent_mail) or ('ok read' in sent_mail) or ('yeah read' in sent_mail) :
                continue
            else :
                self.talk('okay')
                self.get_input()
                break


    def get_input(self) :
        self.talk('Do you need my help?')
        user = self.get_info()
        if ('yes' in user) or ('yeah' in user) or ('yes I need' in user) or ('I need' in user) or ('ok' in user):
            self.talk('What you want to do?')
            user_info = self.get_info()
            if ('send email' in user_info) or ('send a email' in user_info) or ('send mail' in user_info) or ('send a mail' in user_info) :
                self.get_email_info()
            elif ('read email' in user_info) or ('read emails' in user_info) or ('read mail' in user_info) or ('read mails' in user_info) or ('read my emails' in user_info) or ('read my mails' in user_info) :
                self.get_inbox()
                self.talk('!There is no more new Email for you. Thank you, have a nice day!')
                self.get_input()
            elif ('read sent mails' in user_info) or ('read sent emails' in user_info) or ('read sent email' in user_info) or ('read sent mail' in user_info) :
                self.get_sent()
            elif ('nothing' in user_info) or ("don't do anything" in user_info) :
                self.talk('okay')
                self.talk('Thank you, have a nice day.')
            else :
                self.talk("Sorry I can't help you with that.")
        elif ('no' in user) or ("no don't need" in user) or ("I don't need" in user) :
            self.talk('okay')
            self.talk('Thank you, have a nice day.')
        else :
            self.talk("Sorry I can't help you with that.")

    def analyze_user(self) :
        self.talk('Hello! My name is pybot. Do you want to login, or Register your self ')
        face = self.get_info()
        if 'login' in face :
            self.talk("Scanning Face....")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cv2.imwrite('login.jpg', frame)
            cv2.destroyAllWindows()
            cap.release()
            self.talk("Face scan complete.")
            baseimg = face_recognition.load_image_file("register.jpg")
            baseimg = cv2.cvtColor(baseimg, cv2.COLOR_BGR2RGB)

            myface = face_recognition.face_locations(baseimg)[0]
            encodemyface = face_recognition.face_encodings(baseimg)[0]
            cv2.rectangle(baseimg, (myface[3], myface[0]), (myface[1], myface[2]), (255, 0, 255), 2)

            sampleimg = face_recognition.load_image_file("login.jpg")
            sampleimg = cv2.cvtColor(sampleimg, cv2.COLOR_BGR2RGB)

            try :
                samplefacetest = face_recognition.face_locations(sampleimg)[0]
                encodesamplefacetest = face_recognition.face_encodings(sampleimg)[0]
            except IndentationError as e :
                self.talk("Index Error. Authentication Failed")
                sys.exit()

            result = face_recognition.compare_faces([encodemyface], encodesamplefacetest)
            resultstring = str(result)

            if resultstring == "[True]" :
                self.talk("User authenticated!Welcome back sir")
                self.get_input()
            else :
                self.talk("Authentication Failed! Sorry I Can't help you")

        elif 'register' in face :
            self.talk('answer password to proceed')
            password = self.get_info()
            if '123' in password :
                self.talk('password approved')
                self.talk("Scanning Face to register....")
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cv2.imwrite('register.jpg', frame)
                cv2.destroyAllWindows()
                cap.release()
                self.talk("Face scan complete.")
                self.talk('You are registered successfully!')
            else:
                self.talk("wrong password, Sorry I Can't help you")

        else :
            self.talk("Sorry I can't help you with that.")


class PYBOTApp(MDApp) :
    def buid(self) :
        return Pybot()



if __name__ == '__main__' :
    PYBOTApp().run()