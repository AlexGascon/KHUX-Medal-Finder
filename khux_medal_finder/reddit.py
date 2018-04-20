import os
import praw
import prawcore


class RedditService:

    def __init__(self):
        self.reddit = praw.Reddit(user_agent='Medal finder bot by /u/Pawah/',
                                  client_id=os.environ.get('REDDIT_BOT_TOKEN'),
                                  client_secret=os.environ.get('REDDIT_BOT_SECRET'),
                                  username=os.environ.get('REDDIT_BOT_USERNAME'),
                                  password=os.environ.get('REDDIT_BOT_PASSWORD'))

        self.valid = False
        self.validate_authentication()

    def validate_authentication(self):
        """Validates if we are correctly authenticated on Reddit and sets the instance variable 'valid' to the result.

        This is necessary because praw.Reddit returns us Reddit and Subreddit instances as if there hadn't been any
        problem even when the authentication is invalid, and therefore we won't realize if it happens."""
        try:
            self.reddit.user.me()
            self.valid = True

        except prawcore.OAuthException as exception:
            print('Invalid username/password. Verify that the account you\'re using is authorized on the script app')
            self.valid = False
            raise exception

        except prawcore.exceptions.ResponseException as exception:
            print('Invalid auth. Verify your credentials')
            self.valid = False
            raise exception

        # Other errors
        except BaseException as exception:
            self.valid = False
            raise exception

    def subreddit(self, subreddit_name):
        return self.reddit.subreddit(subreddit_name)

    def last_subreddit_comments(self, subreddit_name, amount=1000):
        subreddit = self.reddit.subreddit(subreddit_name)
        return subreddit.comments(limit=amount)
