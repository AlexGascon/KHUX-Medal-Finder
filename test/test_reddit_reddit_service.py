import unittest
from unittest import mock

import os
import praw
import prawcore
import requests_mock

from khux_medal_finder.reddit import RedditService


class TestRedditService(unittest.TestCase):

    def setUp(self):
        self.ENV_MOCK = {
            'REDDIT_BOT_TOKEN': "fake token",
            'REDDIT_BOT_SECRET': "fake bot secret",
            'REDDIT_BOT_USERNAME': "fake username",
            'REDDIT_BOT_PASSWORD':  "fake password",
            'REDDIT_BOT_NAME': "khux_medal_finder",
            'REDDIT_SUBREDDIT': "fake subreddit"
        }

        self.env_patcher = mock.patch.dict(os.environ, self.ENV_MOCK)
        self.env_patcher.start()

    def test_reddit_instantiated_correctly_if_there_are_credentials(self):
        with mock.patch('praw.models.User.me', return_value=None):
            self.assertIsInstance(RedditService().reddit, praw.Reddit)

    def test_subreddit_obtained_correctly_if_there_are_credentials(self):
        with mock.patch('praw.models.User.me', return_value=None):
            self.assertIsInstance(RedditService().subreddit('test'), praw.models.Subreddit)

    def test_reddit_service_valid_if_credentials_are_correct(self):
        # This is correct if it doesn't raise any exception
        with mock.patch('praw.models.User.me', return_value=None):
            reddit = RedditService()
            self.assertTrue(reddit.valid)

    def test_reddit_service_raises_responseexception_if_credentials_are_incorrect(self):
        with mock.patch('praw.models.User.me', side_effect=prawcore.exceptions.ResponseException(mock.Mock(status_code=401))):
            with self.assertRaises(prawcore.exceptions.ResponseException):
                RedditService()

    def test_reddit_service_raises_oauthexception_if_username_isnt_authorized(self):
        with mock.patch('praw.models.User.me', side_effect=prawcore.OAuthException(None, None, None)):
            with self.assertRaises(prawcore.OAuthException):
                RedditService()

    def test_reddit_service_invalid_if_credentials_are_incorrect(self):
        with mock.patch('praw.models.User.me', side_effect=prawcore.exceptions.ResponseException(mock.Mock(status_code=401))):
            with self.assertRaises(prawcore.exceptions.ResponseException):
                reddit = RedditService()
                self.assertFalse(reddit.valid)

    def test_reddit_service_invalid_if_username_isnt_authorized(self):
        with mock.patch('praw.models.User.me', side_effect=prawcore.OAuthException(None, None, None)):
            with self.assertRaises(prawcore.OAuthException):
                reddit = RedditService()
                self.assertFalse(reddit.valid)

    def test_reddit_service_raises_base_exception_if_raised(self):
        with mock.patch('praw.models.User.me', side_effect=BaseException('Exception to be raised')):
            with self.assertRaises(BaseException):
                RedditService()

    def test_reddit_service_raises_other_exceptions_if_raised(self):
        with mock.patch('praw.models.User.me', side_effect=Exception('Inherited exception to be raised')):
            with self.assertRaises(Exception):
                RedditService()

    def test_reddit_service_invalid_if_baseexception_raised(self):
        with mock.patch('praw.models.User.me', side_effect=BaseException('Exception to be raised')):
            with self.assertRaises(BaseException):
                reddit = RedditService()
                self.assertFalse(reddit.valid)

    def test_reddit_service_invalid_if_other_exceptions(self):
        with mock.patch('praw.models.User.me', side_effect=Exception('Inherited exception to be raised')):
            with self.assertRaises(Exception):
                reddit = RedditService()
                self.assertFalse(reddit.valid)

    def tearDown(self):
        self.env_patcher.stop()
