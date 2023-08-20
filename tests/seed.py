from app import app
from models import db, Post, Tag, User



def seed_db():
    db.drop_all()
    db.create_all()

    u1 = User(first_name='Sam', last_name='Houston', 
        image_url='https://upload.wikimedia.org/wikipedia/commons/1/17/Samuel_houston.jpg')
    u2 = User(first_name='Alan', last_name='Alda',
        image_url='https://upload.wikimedia.org/wikipedia/commons/3/3f/Alan_Alda_by_Bridget_Laudien_%28cropped%29.jpg')
    u3 = User(first_name='Anthony', last_name='Fauci',
        image_url='https://upload.wikimedia.org/wikipedia/commons/6/64/Anthony_Fauci.jpg')
    db.session.add_all([u1, u2, u3])
    db.session.commit()

    t1 = Tag(name='Seattle')
    t2 = Tag(name='JavaScript')
    t3 = Tag(name='history')
    db.session.add_all([t1, t2, t3])
    db.session.commit()

    p1 = Post(title='Post 1', content='Here is content 1', user_id=u1.id)
    p1.tags = [t1, t2, t3]
    p2 = Post(title='Post 2', content='Here is content 2', user_id=u1.id)
    p2.tags = [t1, t2]
    p3 = Post(title='Post 3', content='Here is content 3', user_id=u2.id)
    db.session.add_all([p1, p2, p3])
    db.session.commit()


if __name__ == '__main__':
    seed_db()