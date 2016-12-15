import datetime
import random

import praw

from angrates.settings import REDDIT_CLIENT_SECRET, REDDIT_PASSWORD



class Reddit:
    def __init__(self, airdate):
        self.reddit = None
        self.airdate = airdate

    def connect(self):
        self.reddit = praw.Reddit(
            user_agent='ANGBOT (by /u/ben174)',
            client_id='U7NTsh65kdJlZQ',
            client_secret=REDDIT_CLIENT_SECRET,
            username='AnGBingoBot',
            password=REDDIT_PASSWORD,
        )

    def get_body(self):
        body = 'Topics include:\n\n'
        for hour in self.airdate.get_hours():
            body += '**{}:00 - {}**\n\n{}\n\n\n\n'.format(hour.pub_date.hour, hour.title, hour.description)

        footer = ("I'm a freaky-deeky bot. I'll show you SOURCELINK my source if you "
                  "show me yours. I'm made by /u/ben174 @ http://www.bugben.com and my home is "
                  "http://www.armstrongandgettybingo.com - a searchable site full of Armstrong and Getty "
                  "podcasts and clips and other goodness dating back to 2001.")

        # superscript it
        footer = ' ^'.join(footer.split(' '))
        footer.replace('SOURCELINK', '[^my ^source](https://github.com/ben174/angrates)')

        body += '________________________________\n\n^' + footer
        return body

    def create_post(self):
        title = '[AnG] Daily Discussion Thread for {}/{}/{} {}'.format(
            self.airdate.pub_date.month,
            self.airdate.pub_date.day,
            self.airdate.pub_date.year,
            random.randrange(1000, 9999)
        )

        body = self.get_body()

        subreddit = 'ArmstrongAndGetty'
        subreddit = 'test'

        submission = self.reddit.subreddit(subreddit).submit(title, selftext=body)
        self.airdate.reddit_post_id = submission.id
        self.airdate.reddit_url = submission.url
        self.airdate.save()


    def update_post(self):
        submission = self.reddit.submission(self.airdate.reddit_post_id)
        submission.edit(self.get_body())