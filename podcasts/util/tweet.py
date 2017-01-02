import datetime
import random
from urllib2 import urlopen

import twitter

from angrates.settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_KEY, \
    TWITTER_ACCESS_TOKEN_SECRET


class Twitter:
    def __init__(self):
        self.api = None

    def connect(self):
        self.api = twitter.Api(
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET,
            access_token_key=TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
        )

    def post_hour(self, hour):
        result = None

        f = urlopen('http://tinyurl.com/api-create.php?url={0}'.format(hour.get_bingo_url()))
        tiny_url = f.read()

        POST_LENGTH = 140

        body = '<BOD>\n----\nListen @ {}'.format(tiny_url)
        short_desc = hour.description[:POST_LENGTH-(len(body) - 5)]
        body = body.replace('<BOD>', short_desc)

        self.api.PostUpdate(body)
        hour.tweeted = True
        hour.save()

    def post_airdate(self, airdate):
        pass
