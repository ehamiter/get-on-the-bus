## Get on the bus

> Google calendar makes sweet love to your alarm clock

(Inspired from [Raspberry Pi as a Google Calender Alarm Clock](http://www.esologic.com/?p=634))

This year, my kids started riding the school bus, which is super convenient and means I don't have to spend extra time getting them to school. That is, if they make the bus. Sometimes they lose track of time, and I wanted a pretty reliable way of reminding them when it's time to go outside to wait for the big yellow limousine to escort them to school. 

Since I am lazy, I decided to have this automated, which uses (ideally) a Raspberry Pi and Google Calendar to check for 'Get on the bus' events, and fires an appropriately annoying song snippet from The Doodlebops called 'Get on the bus.' It's dynamic in the sense that it will try and play any mp3 with the event title, and falls back to a default mp3 (my default.mp3 is an old school Nokia ringtone-- of course, you can make yours anything you wish).

1. Install [mpg123](http://sourceforge.net/projects/mpg123/files/):

        ./configure
        make
        make install

2. Install the requirements:

        pip install -r requirements.txt

3. Create a new project on the [Google Developers Console](https://console.developers.google.com)
4. Enable the Calendars API
5. Create new Client ID for web application and download the JSON as `client_secrets.json`
6. Create a new key for browser application and paste the `API KEY` value in `alarm.py`'s `API_KEY` variable
7. Create a new Google calendar and paste the ID in `alarm.py`'s `CALENDAR_ID` variable
8. Run the program: `python alarm.py`

All new events will try to play the name of the event as an mp3 file in the `mp3s` folder with spaces converted to underscores, i.e.:  

`Get on the bus` == `mp3s/get_on_the_bus.mp3`  

If the event has no corresponding mp3 file, `default.mp3` will play.
