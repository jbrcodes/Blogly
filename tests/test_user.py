from unittest import TestCase

from app import app
from models import db, User
from .seed import seed_db



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


class UserTestCase(TestCase):


    def setUp(self):
        seed_db()


    def tearDown(self):
        # This seems to be necessary to keep later tests from hanging
        # (Maybe I can't drop_all() if a transaction is in progress?)
        db.session.rollback()


    # -----------------------------------------------------


    def test_instantiate(self):
        user = User(first_name='Maggie', last_name='Mama', image_url='http://foo.com/me.jpg')
        self.assertEqual(user.first_name, 'Maggie')
        self.assertEqual(user.full_name, 'Maggie Mama')


    def test_new(self):
        user = User(first_name='Maggie', last_name='Mama', image_url='http://foo.com/me.jpg')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 4)


    def test_edit(self):
        user = User.query.get(1)  # Sam Houston
        user.last_name = 'Denver'
        db.session.commit()
        users = User.query.filter_by(last_name='Denver').all()
        self.assertEqual(len(users), 1)
    

    def zztest_delete(self):
        self.assertEqual(User.query.count(), 3)
        user = User.query.get(1)
        db.session.delete(user)
        self.assertEqual(User.query.count(), 2)
