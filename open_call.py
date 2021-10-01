import time
from urllib.request import urlopen
import datetime
from bs4 import BeautifulSoup
import requests
import sys
import argparse

import config
import mail

URL = config.URL

def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--update-rate", "-t", type=int, default=3600,
                        help="Update rate in seconds")
    return parser.parse_args(args)


def get_update_date():
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html.parser")
    results = soup.find_all("div", class_="aalto-user-generated-content")
    
    date = results[2].find('p').find('strong').text.strip()[:-1]
    return date.replace('.', '/')
    

def main(args):
    mails = config.MAILS
    subject = 'AYY OPEN CALL'

    email = mail.Mail()

    last_update = get_update_date()
    
    print('=== Monitoring Started ===')
    print('Last Update: {}, Check Every: {}, Email Notification: {}'.format(last_update, args.update_rate, mails))
    
    while True:
        try:
            time.sleep(args.update_rate)
            updated_date = get_update_date()
            if updated_date == last_update:
                print('{}, No new announcement. AYY\'s Last update: {}'.format(datetime.datetime.now().strftime("%X, %x"), last_update))
            else:
                content = 'Website was updated recently. There might be new house options.'
                print('{}'.format(datetime.datetime.now().strftime("%X, %x")), content)
                email.send(mails, subject, content)
                print('Mailing list has been alerted.')
                last_update = get_update_date()

        except Exception as e:
            content = 'There was an exception! \n {}. The script has been terminated.'.format(e)
            print('!--- {}'.format(datetime.datetime.now().strftime("%X, %x")), content, '---!')
            email.send(mails, subject, content)
            print('Mailing list has been alerted.')
            break
        
if __name__ == "__main__":
    args = parse_args()
    main(args)
        
