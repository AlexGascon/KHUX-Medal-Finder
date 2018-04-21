import os
import praw
import prawcore

from khux_medal_finder import helpers
from khux_medal_finder.models import Comment, Reply


class RedditService:
    REPLY_BOT_DESCRIPTION = "\n\nBeeep bop. I'm a bot! I've been created by Pawah and you can find my code on Github"
    REPLY_NO_MEDALS = "I'm sorry, I couldn't find any medal that match your requirements." + REPLY_BOT_DESCRIPTION

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

    def reply(self, comment, medals):
        if medals:
            success = True
            reply_body = helpers.prepare_reply_body(medals) + self.REPLY_BOT_DESCRIPTION
        else:
            success = False
            reply_body = self.REPLY_NO_MEDALS

        reply = comment.reply(reply_body)

        comment_object = Comment.create(author=comment.author, comment_id=comment.id, text=comment.body,
                                        timestamp=comment.created, url=comment.permalink)
        reply_object = Reply.create(original_comment=comment_object, success=success, comment_id=reply.id,
                                    text=reply_body, timestamp=reply.created, url=reply.permalink)

        return reply_object