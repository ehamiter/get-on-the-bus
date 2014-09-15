# Inspired from 'Raspberry Pi as a Google Calender Alarm Clock'
# http://www.esologic.com/?p=634

from datetime import datetime
import logging, os, platform, re, time

from apiclient.discovery import build
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

from config import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Alarm():
    system = platform.system().lower()
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE,
                                   scope='https://www.googleapis.com/auth/calendar',
                                   redirect_uri='http://localhost:8080/')

    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = run(flow, storage)

    # Google Calendar service connection
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build(serviceName='calendar', version='v3', http=http, developerKey=API_KEY)

    def check_credentials(self):
        if self.credentials is None or self.credentials.invalid == True:
            credentials = run(self.flow, self.storage)

    def calendar_event_query(self):
        self.check_credentials()
        today = datetime.today()
        events = self.service.events().list(singleEvents=True, calendarId=CALENDAR_ID).execute()

        for i, event in enumerate(events['items']):
            name = event['summary'].lower()
            start = event['start']['dateTime'][:-9]
            description = event.get('description', '')
            repeat = True if description.lower() == 'repeat' else False
            now = today.strftime('%Y-%m-%dT%H:%M')

            if start >= now:
                logger.debug('Event #%s, Name: %s, Start: %s', i, name, start)

                if start == now:
                    if name.startswith('say'):
                        name = re.sub(r'[^a-zA-Z0-9\s\']', '', name)
                        command = '{0} "{1}"'.format('say' if system == 'darwin' else 'espeak -ven+m2', name[4:])
                        logger.info('Event starting. Announcing \'%s\'...', name[4:])
                    else:
                        mp3_files = os.listdir(MP3_FOLDER)
                        mp3_name = name.replace(' ', '_') + '.mp3'
                        mp3_name = mp3_name if mp3_name in mp3_files else 'default.mp3'
                        command = 'mpg123 \'{}/{}\''.format(MP3_FOLDER, mp3_name)
                        logger.info('Event %s starting. Playing mp3 file %s...', name, mp3_name)
                    os.system(command)
                    if repeat == False:
                        time.sleep(60)

    def poll(self):
        logger.info('Polling calendar for events...')
        self.calendar_event_query()


while True:
    a = Alarm()
    a.poll()
    time.sleep(FREQUENCY_CHECK)
