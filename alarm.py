# Inspired from 'Raspberry Pi as a Google Calender Alarm Clock'
# http://www.esologic.com/?p=634

from datetime import datetime
import logging, os, platform, re, time

from apiclient.discovery import build
from apscheduler.schedulers.blocking import BlockingScheduler
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

from config import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
FREQUENCY_CHECK = 10 # in seconds
MP3_FOLDER = 'mp3s'

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

# Main
def calendar_event_query():
    today = datetime.today()
    events = service.events().list(singleEvents=True, calendarId=CALENDAR_ID).execute()

    for i, event in enumerate(events['items']):
        event_name = event['summary'].lower()
        event_start = event['start']['dateTime'][:-9]
        event_description = event.get('description', '')
        repeat = True if event_description.lower() == 'repeat' else False
        now = today.strftime('%Y-%m-%dT%H:%M')

        if event_start >= now:
            logger.debug('Event #%s, Event Name: %s, Event Start: %s', i, event_name, event_start)

            if event_start == now:
                if event_name.startswith('say'):
                    event_name = re.sub(r'[^a-zA-Z0-9\s\']', '', event_name)
                    command = '{0} "{1}"'.format('say' if system == 'darwin' else 'espeak -ven+m2', event_name[4:])
                    logger.info('Event starting. Announcing \'%s\'...', event_name[4:])
                else:
                    mp3_files = os.listdir(MP3_FOLDER)
                    mp3_name = event_name.replace(' ', '_') + '.mp3'
                    mp3_name = mp3_name if mp3_name in mp3_files else 'default.mp3'
                    command = 'mpg123 \'{}/{}\''.format(MP3_FOLDER, mp3_name)
                    logger.info('Event %s starting. Playing mp3 file %s...', event_name, mp3_name)
                os.system(command)
                if repeat == False:
                    time.sleep(60)

def poll():
    logger.info('Polling calendar for events...')
    calendar_event_query()

scheduler = BlockingScheduler()
scheduler.add_job(poll, 'interval', seconds=FREQUENCY_CHECK)
scheduler.start()
