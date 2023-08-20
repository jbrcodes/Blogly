from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func



db = SQLAlchemy()

# Doing it Colt's Way (versus Armin's Way)
def connect_db(app):
    db.app = app
    db.init_app(app)



# -----------------------------------------------------------------------------


class User(db.Model):

    # SQLAlchemy

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

    posts = db.relationship('Post', backref='user', cascade='delete')

    def __repr__(self):
        s = self
        return f"<User {s.id} '{s.full_name}'>"


    # My Stuff

    editable_attrs = ('first_name', 'last_name', 'image_url')


    def update(self, adict):
        for key in User.editable_attrs:
            if key in adict:
                setattr(self, key, adict[key])


    @property
    def full_name(self):
        return f'{ self.first_name } { self.last_name }'


# -----------------------------------------------------------------------------


class Post(db.Model):

    # SQLAlchemy

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        s = self
        return f"<Post {s.id} '{s.title}'>"


    # My Stuff

    editable_attrs = ('title', 'content', 'user_id')


    def update(self, adict):
        for key in Post.editable_attrs:
            if key in adict:
                setattr(self, key, adict[key])

        # Handle tags separately
        tag_names = adict.getlist('tags')  # array of tag names
        self.tags = Tag.query.filter( Tag.name.in_(tag_names) ).all()


# -----------------------------------------------------------------------------


class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)

    posts = db.relationship('Post', backref='tags', secondary='posts_tags')

    def __repr__(self):
        s = self
        return f"<Tag {s.id} '{s.name}'>'"


    # My Stuff

    editable_attrs = ('name',)


    def update(self, adict):
        for key in Tag.editable_attrs:
            if key in adict:
                setattr(self, key, adict[key])


class PostTag(db.Model):
    '''Junction/association table for many-to-many between Post and Tag'''

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)