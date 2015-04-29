# Notice: This code and the corresponding google API have changed several times since this was first published. It is currently not stable, so do not rely on this being reliable or even working. I will try and remedy the stability of it, but currently this is low on my list of priorities.

## Get on the bus

> Google calendar makes sweet love to your alarm clock

(Inspired from [Raspberry Pi as a Google Calender Alarm Clock](http://www.esologic.com/?p=634))

This year, my kids started riding the school bus, which is super convenient and means I don't have to spend extra time getting them to school. That is, if they make the bus. Sometimes they lose track of time, and I wanted a pretty reliable way of reminding them when it's time to go outside to wait for the big yellow limousine to escort them to school. 

Since I am lazy, I decided to have this automated, which uses (ideally) a Raspberry Pi and Google Calendar to check for events that start with 'say' or have corresponding mp3 titles.

For example:

1. An event titled `say Don't forget to brush your teeth` will announce the phrase 'Don't forget to brush your teeth'.
2. An event with the title `Get on the bus` fires an appropriately annoying song snippet from the mp3s folder by The Doodlebops called `get_on_the_bus.mp3`.

It's dynamic in the sense that it will try and play any mp3 with the event title, and falls back to a default mp3 (my default.mp3 is an old school Nokia ringtone-- of course, you can make yours anything you wish).

Pre-requisite: `mpg123`
  * If you're on Linux, you can install `mpg123` via apt-get:

    ```sh
    sudo apt-get install mpg123
    ```

  * If you're on OS X, you can install `mpg123` via [Homebrew](http://brew.sh):

    ```sh
    brew install mpg123
    ```

  * Or you can download the [source](http://sourceforge.net/projects/mpg123/files/) and run:

    ```sh
    ./configure
    make
    make install
    ```

Pre-requisite for Linux text to speech: `espeak`

    sudo apt-get install espeak

1. Install the requirements:

        pip install -r requirements.txt

2. Create a new project on the [Google Developers Console](https://console.developers.google.com)
3. Enable the Calendars API
4. Create the file `config.py`
5. Create new Client ID for web application and download the JSON as `client_secrets.json` and set `CLIENT_SECRET_FILE = 'client_secrets.json'` in `config.py`
6. Create a new key for browser application and set the `API KEY` value as `API_KEY = xxx` in `config.py`
7. Create a new Google calendar and set the ID as `CALENDAR_ID = xxx` in `config.py` (Click drop-down arrow by calendar name; choose 'Calendar Settings'; find ID by 'Calendar Address' section)
8. Add `FREQUENCY_CHECK` (in seconds) and `MP3_FOLDER` location in `config.py`.
9. Run the program: `python alarm.py`

All new events will try to play the name of the event as an mp3 file in the `mp3s` folder with spaces converted to underscores, i.e.:  

`Get on the bus` == `mp3s/get_on_the_bus.mp3`  

If the event has no corresponding mp3 file, `default.mp3` will play. To have the sound play repeatedly until the event's time expires, enter `repeat` as the event's description.

Example `config.py` file:

    API_KEY = '123456789qwertyuiop987654321asdfghjkl54321'
    CALENDAR_ID = 'mnbvcxzlkjhgfdsa123@group.calendar.google.com'
    CLIENT_SECRET_FILE = 'client_secrets.json'
    FREQUENCY_CHECK = 5 # in seconds
    MP3_FOLDER = 'mp3s'
