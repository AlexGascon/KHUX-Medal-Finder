import os
import praw
import prawcore
import unittest
import peewee
from unittest import mock
from datetime import datetime

from khux_medal_finder import helpers
from khux_medal_finder.models import Comment, Reply
from khux_medal_finder.reddit import RedditService

ENV_MOCK = {
    'REDDIT_BOT_TOKEN': "fake token",
    'REDDIT_BOT_SECRET': "fake bot secret",
    'REDDIT_BOT_USERNAME': "fake username",
    'REDDIT_BOT_PASSWORD': "fake password",
    'REDDIT_BOT_NAME': "khux_medal_finder",
    'REDDIT_SUBREDDIT': "fake subreddit"
}


class TestRedditServiceInitialization(unittest.TestCase):

    def setUp(self):
        self.env_patcher = mock.patch.dict(os.environ, ENV_MOCK)
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


class TestRedditService(unittest.TestCase):


    def setUp(self):
        self.env_patcher = mock.patch.dict(os.environ, ENV_MOCK)
        self.env_patcher.start()

        with mock.patch('praw.models.User.me', return_value=None):
            self.reddit = RedditService()

        # Bind model classes to test db
        self.test_db = peewee.SqliteDatabase(':memory:')
        self.MODELS = [Comment, Reply]
        for model in self.MODELS:
            model.bind(self.test_db, bind_refs=False, bind_backrefs=False)

        self.test_db.connect()
        self.test_db.create_tables(self.MODELS)

        mock_comment = mock.Mock()
        mock_comment.author = 'Francisco Umbral'
        mock_comment.id = 'abcdex'
        mock_comment.body = 'Yo he venido aqui a hablar de mi libro'
        mock_comment.created = 1
        mock_comment.permalink = 'https://yo.hevenidoaquiahablardemi.libro/comentario/11234/'
        self.mock_comment = mock_comment

        mock_reply = mock.Mock()
        mock_reply.id = 'xedcba'
        mock_reply.created = 2
        mock_reply.permalink = 'https://medium.com/alexgascon'
        self.mock_reply = mock_reply

    def tearDown(self):
        self.test_db.drop_tables(self.MODELS)
        self.test_db.close()

        self.env_patcher.stop()

    def test_reply_if_there_arent_medals_responds_with_the_correct_text(self):
        self.mock_comment.reply.return_value = self.mock_reply
        expected_reply_body = "I'm sorry, I couldn't find any medal that match your requirements." + "\n\nBeeep bop. I'm a bot! I've been created by Pawah and you can find my code on Github"

        self.reddit.reply(self.mock_comment, [])

        self.mock_comment.reply.assert_called_once_with(expected_reply_body)

    def test_reply_if_there_arent_medals_creates_comment_object_with_the_correct_attributes(self):
        self.mock_comment.reply.return_value = self.mock_reply

        self.reddit.reply(self.mock_comment, [])
        last_comment = Comment.select().order_by(-Comment.id).get()

        self.assertEqual(last_comment.author, 'Francisco Umbral')
        self.assertEqual(last_comment.comment_id, 'abcdex')
        self.assertEqual(last_comment.text, 'Yo he venido aqui a hablar de mi libro')
        self.assertEqual(last_comment.timestamp, datetime.fromtimestamp(1))
        self.assertEqual(last_comment.url, 'https://yo.hevenidoaquiahablardemi.libro/comentario/11234/')

    def test_reply_if_there_arent_medals_creates_reply_object_with_the_correct_attributes(self):
        self.mock_comment.reply.return_value = self.mock_reply
        expected_reply_body = "I'm sorry, I couldn't find any medal that match your requirements.\n\nBeeep bop. I'm a bot! I've been created by Pawah and you can find my code on Github"

        self.reddit.reply(self.mock_comment, [])
        obtained_reply = Reply.select().order_by(-Reply.id).get()
        last_comment = Comment.select().order_by(-Comment.id).get()

        self.assertFalse(obtained_reply.success)
        self.assertEqual(obtained_reply.original_comment, last_comment)
        self.assertEqual(obtained_reply.author, 'khux_medal_finder')
        self.assertEqual(obtained_reply.comment_id, 'xedcba')
        self.assertEqual(obtained_reply.text, expected_reply_body)
        self.assertEqual(obtained_reply.timestamp, datetime.fromtimestamp(2))
        self.assertEqual(obtained_reply.url, 'https://medium.com/alexgascon')

    def test_reply_if_there_are_medals_responds_with_the_correct_text(self):
        self.mock_comment.reply.return_value = self.mock_reply
        mock_medal = mock.Mock()
        helper_reply = "Mocked response"
        bot_presentation_text = "\n\nBeeep bop. I'm a bot! I've been created by Pawah and you can find my code on Github"

        with mock.patch('khux_medal_finder.helpers.prepare_reply_body', return_value=helper_reply):
            self.reddit.reply(self.mock_comment, [mock_medal])

        self.mock_comment.reply.assert_called_once_with(helper_reply + bot_presentation_text)

    def test_reply_if_there_are_medals_creates_comment_object_with_the_correct_attributes(self):
        self.mock_comment.reply.return_value = self.mock_reply
        self.mock_comment.reply.return_value = self.mock_reply
        mock_medal = mock.Mock()

        self.reddit.reply(self.mock_comment, [mock_medal])
        last_comment = Comment.select().order_by(-Comment.id).get()

        self.assertEqual(last_comment.author, 'Francisco Umbral')
        self.assertEqual(last_comment.comment_id, 'abcdex')
        self.assertEqual(last_comment.text, 'Yo he venido aqui a hablar de mi libro')
        self.assertEqual(last_comment.timestamp, datetime.fromtimestamp(1))
        self.assertEqual(last_comment.url, 'https://yo.hevenidoaquiahablardemi.libro/comentario/11234/')

    def test_reply_if_there_are_medals_creates_reply_object_with_the_correct_attributes(self):
        self.mock_comment.reply.return_value = self.mock_reply
        self.mock_comment.reply.return_value = self.mock_reply
        mock_medal = mock.Mock()
        helper_reply = "Mocked response"
        bot_presentation_text = "\n\nBeeep bop. I'm a bot! I've been created by Pawah and you can find my code on Github"

        with mock.patch('khux_medal_finder.helpers.prepare_reply_body', return_value=helper_reply):
            self.reddit.reply(self.mock_comment, [mock_medal])
        obtained_reply = Reply.select().order_by(-Reply.id).get()
        last_comment = Comment.select().order_by(-Comment.id).get()

        self.assertTrue(obtained_reply.success)
        self.assertEqual(obtained_reply.original_comment, last_comment)
        self.assertEqual(obtained_reply.author, 'khux_medal_finder')
        self.assertEqual(obtained_reply.comment_id, 'xedcba')
        self.assertEqual(obtained_reply.text, helper_reply + bot_presentation_text)
        self.assertEqual(obtained_reply.timestamp, datetime.fromtimestamp(2))
        self.assertEqual(obtained_reply.url, 'https://medium.com/alexgascon')

    def test_reply_if_there_is_an_error_commenting_doesnt_create_comment_object(self):
        self.mock_comment.reply.side_effect = Exception("Network Error")

        with self.assertRaises(Exception):
            self.reddit.reply(self.mock_comment, [])

        comments_amount = Comment.select().order_by(-Comment.id).count()
        self.assertEqual(comments_amount, 0)

    def test_reply_if_there_is_an_error_commenting_doesnt_create_reply_object(self):
        self.mock_comment.reply.side_effect = Exception("Network Error")

        with self.assertRaises(Exception):
            self.reddit.reply(self.mock_comment, [])

        replies_amount = Reply.select().order_by(-Reply.id).count()
        self.assertEqual(replies_amount, 0)
