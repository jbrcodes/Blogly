from unittest import TestCase

from app import app
from models import db, Post, Tag
from .seed import seed_db



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


class TagTestCase(TestCase):


    def setUp(self):
        seed_db()


    def tearDown(self):
        # This seems to be necessary to keep later tests from hanging
        # (Maybe I can't drop_all() if a transaction is in progress?)
        db.session.rollback()


    # -----------------------------------------------------


    def test_relation(self):
        post = Post.query.get(1)
        self.assertEqual(len(post.tags), 3)
        tag = Tag.query.get(1)
        self.assertEqual(len(tag.posts), 2)


    def test_new(self):
        tag = Tag(name='Cheetos')
        db.session.add(tag)
        db.session.commit()
        self.assertEqual(Tag.query.count(), 4)


    def test_edit(self):
        tag = Tag.query.get(1)
        tag.name = 'Boston'
        db.session.commit()
        tags = Tag.query.filter_by(name='Boston').all()
        self.assertEqual(len(tags), 1)
    

    def test_delete(self):
        self.assertEqual(Tag.query.count(), 3)
        db.session.delete( Tag.query.get(2) )
        self.assertEqual(Tag.query.count(), 2)