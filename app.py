"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def users():
    """ Home page, lists all existing users """
    users = User.query.all()
    return render_template('index.html', users = users)

@app.route('/users/new')
def users_new():
    """ Page to add new user"""
    return render_template('create_user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """ Form post to add new user """
    first = request.form["first"]
    last = request.form["last"]
    image = request.form["image"]
    if image:
        new_user = User(first_name=first, last_name=last, image_url=image)
    else:
        new_user = User(first_name=first, last_name=last)
    

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>')
def user_profile(id):
    """ Individual user page """
    user = User.query.get(id)

    return render_template('existing_user.html', user=user)

@app.route('/users/<int:id>/edit')
def edit_user(id):
    """ Edit individual user page """
    user = User.query.get(id)
    return render_template('/edit_form.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def save_edit_user(id):
    """ Form post to edit individual user page """
    user = User.query.get(id)

    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    if request.form["image"]:
        user.image_url = request.form["image"]
    
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>/delete', methods=["POST"])
def delete_user(id):
    """ Form post to delete a user """
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:id>/posts/new')
def new_post_form(id):
    """ Page for individual user to add new post """
    user = User.query.get(id)
    return render_template("new_post.html", user=user)


@app.route('/users/<int:id>/posts/new', methods=['POST'])
def submit_new_post(id):
    """ Form post for adding new post for individual user """
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, author_id=id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{id}")
