import requests
import time
import config
import smtplib
import hashlib
from urllib.request import urlopen
import ssl

url = config.URL
response = urlopen(url).read()
currentHash = hashlib.sha224(response).hexdigest()


class Mail:
    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = config.USERNAME
        self.password = config.PASSOWRD

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        
        for email in emails:
            result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")

        service.quit()

mails = config.MAILS
subject = 'AYY OPEN CALL'
content = 'Something changed'

mail = Mail()

response = urlopen(url).read()
currentHash = hashlib.sha224(response).hexdigest()
while True:

    try:
        time.sleep(1800)
        response = urlopen(url).read()
        newHash = hashlib.sha224(response).hexdigest()

        if newHash == currentHash:
            continue

        else:
            print('something changed!')
            mail.send(mails, subject, content)
            response = urlopen(url).read()
            currentHash = hashlib.sha224(response).hexdigest()
            continue

    except Exception as e:

        print(e)