# test_db.py

import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict

from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory database only live
        # for the duration of the connection, and in the next step we close
        # the connection... but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2
        # Get timeline posts and assert that they are correct
        posts = {
            'timeline_posts': [
                model_to_dict(p)
                for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
        }
        self.assertEqual(posts['timeline_posts'][0]['id'], second_post.id, 'First post is not the same')
        self.assertEqual(posts['timeline_posts'][0]['name'], second_post.name, 'Incorrect name for first timeline post')
        self.assertEqual(posts['timeline_posts'][0]['email'], second_post.email, 'Incorrect email for first timeline post')
        self.assertEqual(posts['timeline_posts'][0]['content'], second_post.content, 'Incorrect content for first timeline post')
        self.assertEqual(posts['timeline_posts'][1]['id'], first_post.id, 'Incorrect id for second timeline post')
        self.assertEqual(posts['timeline_posts'][1]['name'], first_post.name, 'Incorrect name for second timeline post')
        self.assertEqual(posts['timeline_posts'][1]['email'], first_post.email, 'Incorrect email for second timeline post')
        self.assertEqual(posts['timeline_posts'][1]['content'], first_post.content, 'Incorrect content for second timeline post')



    if __name__ == '__main__':
        unittest.main()