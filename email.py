import smtplib
import ssl
import config

class Mail:
    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = config.USERNAME
        self.password = config.PASSWORD

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        
        for email in emails:
            result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")

        service.quit()
