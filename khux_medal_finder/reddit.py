import os
import praw


class RedditService:

    def __init__(self):
        self.reddit = praw.Reddit(user_agent='Medal finder bot by /u/Pawah/',
                                  client_id=os.environ.get('_34s5N6yFVugMA'),
                                  client_secret=os.environ.get('REDDIT_BOT_SECRET'),
                                  username=os.environ.get('REDDIT_BOT_USERNAME'),
                                  password=os.environ.get('REDDIT_BOT_PASSWORD'))

        self.subreddit = self.reddit.subreddit(os.environ.get('REDDIT_SUBREDDIT'))

    @property
    def comments(self):
        return self.subreddit.comments()