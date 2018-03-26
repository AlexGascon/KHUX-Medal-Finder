import unittest
from unittest import mock

import os
import praw
import requests_mock

from khux_medal_finder.reddit import RedditService


class TestRedditService(unittest.TestCase):

    def setUp(self):
        self.ENV_MOCK = {
            'REDDIT_BOT_USERNAME': "fake username",
            'REDDIT_BOT_PASSWORD':  "fake password",
            'REDDIT_BOT_TOKEN': "fake token",
            'REDDIT_BOT_SECRET': "fake bot secret",
            'REDDIT_BOT_NAME': "khux_medal_finder",
            'REDDIT_SUBREDDIT': "fake subreddit"
        }

        self.patcher = mock.patch.dict(os.environ, self.ENV_MOCK)
        self.patcher.start()

    def test_reddit_instantiated_correctly_if_there_are_credentials(self):
        with mock.patch('praw.models.User.me', return_value=None):
            self.assertIsInstance(RedditService().reddit, praw.Reddit)

    def test_subreddit_instantiated_correctly_if_there_are_credentials(self):
        with mock.patch('praw.models.User.me', return_value=None):
            self.assertIsInstance(RedditService().subreddit, praw.models.Subreddit)

    def tearDown(self):
        self.patcher.stop()
