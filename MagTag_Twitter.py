# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries.
# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries.
#
# SPDX-License-Identifier: Unlicense

# Display Twitter account tweets on the MagTag
# randomly display Tweets with each wakeup cycle

import time
from adafruit_magtag.magtag import MagTag
from random import randint

try:
    from secrets import secrets
except ImportError:
    print(
        """WiFi settings are kept in secrets.py, please add them there!
the secrets dictionary must contain 'ssid' and 'password' at a minimum"""
    )
    raise

# Set to the twitter username you'd like to fetch tweets from
TwitterList = ['@iPhoneinCanada', '@HKWORLDCITY', '@CPHO_Canada', '@BLOGTO',
                '@torontodotcom', '@adafruit', '@DailyHiveTO', '@RedFlagDeals',
                '@MobileSyrup', '@BMWMOA', 'BMWMotorradCA', '@CircuitPython']
TWITTER_USERNAME = TwitterList[randint(0,11)]

# Set to the amount of time to deep sleep for, in minutes
SLEEP_TIME = 15

# Set up where we'll be fetching data from
DATA_SOURCE = (
    "https://api.twitter.com/1.1/statuses/user_timeline.json?"
    "screen_name=%s&count=1&tweet_mode=extended" % TWITTER_USERNAME
)
TWEET_TEXT = [0, "full_text"]
TWEET_FULL_NAME = [0, "user", "name"]
TWEET_HANDLE = [0, "user", "screen_name"]

magtag = MagTag(url=DATA_SOURCE, json_path=(TWEET_FULL_NAME, TWEET_HANDLE, TWEET_TEXT))
# Set Twitter OAuth2.0 Bearer Token
bearer_token = secrets["twitter_bearer_token"]
magtag.set_headers({"Authorization": "Bearer " + bearer_token})

# Display setup
magtag.set_background("/images/background.bmp")  # Note subdirectory on circuitPY

# Twitter name
magtag.add_text(
    text_position=(70, 10),
    text_font="/fonts/Arial-Bold-12.pcf",
)

# Twitter handle (@username)
magtag.add_text(
    text_position=(70, 30),
    text_font="/fonts/Arial-Italic-12.bdf",
    text_transform=lambda x: "@%s" % x,
)

# Tweet text
magtag.add_text(
    text_font="/fonts/helvB12.bdf",
    text_wrap=45,
    text_maxlen=200,
    text_position=(
        5,
        (magtag.graphics.display.height // 2) + 20,
    ),
    line_spacing=0.75,
)

# preload characters
magtag.preload_font()

try:
    value = magtag.fetch()
    print("Response is", value)
except (ValueError, RuntimeError) as e:
    print("Some error occured, retrying! -", e)

time.sleep(2)
print("Sleeping!")
magtag.exit_and_deep_sleep(SLEEP_TIME * 60)