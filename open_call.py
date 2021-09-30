import time
from urllib.request import urlopen
import datetime
from bs4 import BeautifulSoup
import requests

import config
import mail

url = config.URL
mails = config.MAILS
subject = 'AYY OPEN CALL'

mail = mail.Mail()

def get_update_date():
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    results = soup.find_all("div", class_="aalto-user-generated-content")
    
    date = results[2].find('p').find('strong').text.strip()[:-1]
    return date.replace('.', '/')
    
last_update = get_update_date()

while True:
    try:
        time.sleep(60)
        updated_date = get_update_date()
        if updated_date == last_update:
            print('{}, No new announcement. AYY\'s Last update: {}'.format(datetime.datetime.now().strftime("%X, %x"), last_update))
        else:
            content = 'Website was updated recently. There might be new house options.'
            print('{}'.format(datetime.datetime.now().strftime("%X, %x")), content)
            mail.send(mails, subject, content)
            print('Mailing list has been alerted.')
            last_update = get_update_date()

    except Exception as e:
        content = 'There was an exception! \n {}. The script has been terminated.'.format(e)
        print('!--- {}'.format(datetime.datetime.now().strftime("%X, %x")), content, '---!')
        mail.send(mails, subject, content)
        print('Mailing list has been alerted.')
        break
