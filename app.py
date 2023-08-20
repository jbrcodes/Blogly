import os
from flask import Flask, redirect, render_template, request, url_for
from models import db, connect_db, Post, Tag, User
from jinja import init_app as jinja_init_app



app = Flask(__name__)

app.config['SECRET_KEY'] = \
    os.environ.get('SECRET_KEY', 'I do NOT like SPAM!')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    os.environ.get('DATABASE_URL', 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

jinja_init_app(app)
connect_db(app)
# See NOTES
# with app.app_context():
#     db.create_all()


# -----------------------------------------------------------------------------


@app.route('/')
def home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('home.html', posts=posts)


@app.route('/users')
def list_users():
    users = User.query.order_by(User.last_name).all()

    return render_template('user_list.html', users=users)


@app.route('/users/<int:id>')
def show_user(id):
    user = User.query.get_or_404(id)
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()

    return render_template('user_detail.html', user=user, posts=posts)


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        return render_template('user_form.html')
    else:
        user = User()
        user.update(request.form)
        db.session.add(user)
        db.session.commit()

        return redirect('/users')


@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('user_form.html', user=user)
    else:
        user.update(request.form)
        db.session.commit()

        return redirect('/users')


@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    '''NOTE: We use HTTP POST because DELETE would require JS...'''
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


# -----------------------------------------------------------------------------


@app.route('/posts')
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template('post_list.html', posts=posts)


@app.route('/posts/<int:id>')
def show_post(id):
    post = Post.query.get_or_404(id)

    return render_template('post_detail.html', post=post, post_tags=post.tags)


@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        all_tags = Tag.query.all()
        return render_template('post_form.html', user=user, all_tags=all_tags)
    else:
        post = Post()
        post.update(request.form)
        post.user_id = user_id
        db.session.add(post)
        db.session.commit()

        return redirect( url_for('show_user', id=user_id) )


@app.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'GET':
        all_tags = Tag.query.all()
        return render_template('post_form.html', post=post, post_tags=post.tags, all_tags=all_tags)
    else:
        post.update(request.form)
        db.session.commit()

        return redirect( url_for('show_post', id=id) )


@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    '''NOTE: We use HTTP POST because DELETE would require JS...'''
    post = Post.query.get_or_404(id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect( url_for('show_user', id=user_id) )


# -----------------------------------------------------------------------------


@app.route('/tags')
def list_tags():
    #tags = Tag.query.order_by(collate(Tag.name, 'NOCASE')).all()  # doesn't work
    tags = Tag.query.order_by(Tag.name).all()

    return render_template('tag_list.html', tags=tags)


@app.route('/tags/<int:id>')
def show_tag(id):
    tag = Tag.query.get_or_404(id)

    return render_template('tag_detail.html', tag=tag, posts=tag.posts)


@app.route('/tags/new', methods=['GET', 'POST'])
def new_tag():
    if request.method == 'GET':
        return render_template('tag_form.html')
    else:
        tag = Tag()
        tag.update(request.form)
        db.session.add(tag)
        db.session.commit()

        return redirect( url_for('show_tag', id=tag.id) )


@app.route('/tags/<int:id>/edit', methods=['GET', 'POST'])
def edit_tag(id):
    tag = Tag.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('tag_form.html', tag=tag)
    else:
        tag.update(request.form)
        db.session.commit()

        return redirect( url_for('show_tag', id=id) )


@app.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    '''NOTE: We use HTTP POST because DELETE would require JS...'''
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()

    return redirect( url_for('list_tags') )