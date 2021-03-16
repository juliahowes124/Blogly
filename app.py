"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    """ Render custom 404 error page """

    return render_template('404.html')


@app.route('/')
def index():
    """ Homepage, lists 5 most recent posts """
    posts = Post.query.order_by(Post.created_at.desc()).limit(5)
    return render_template('homepage.html', posts=posts)


@app.route('/users')
def users():
    """ Lists all existing users """
    users = User.query.order_by(User.last_name, User.first_name)
    return render_template('index.html', users=users)


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
    flash("New user created!", 'success')

    return redirect('/users')

@app.route('/users/<int:id>')
def user_profile(id):
    """ Individual user page """
    user = User.query.get_or_404(id)

    return render_template('existing_user.html', user=user)

@app.route('/users/<int:id>/edit')
def edit_user(id):
    """ Edit individual user page """
    user = User.query.get_or_404(id)
    return render_template('/edit_form.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def save_edit_user(id):
    """ Form post to edit individual user page """
    user = User.query.get_or_404(id)

    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    if request.form["image"]:
        user.image_url = request.form["image"]
    
    db.session.commit()
    flash("User successfully edited!", 'success')
    return redirect('/users')

@app.route('/users/<int:id>/delete', methods=["POST"])
def delete_user(id):
    """ Form post to delete a user """
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", 'success')
    return redirect('/users')

@app.route('/users/<int:id>/posts/new')
def new_post_form(id):
    """ Page for individual user to add new post """
    user = User.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template("create_post.html", user=user, tags=tags)


@app.route('/users/<int:id>/posts/new', methods=['POST'])
def submit_new_post(id):
    """ Form post for adding new post for individual user """
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, author_id=id)

    tags = Tag.query.all()
    for tag in tags:
        if request.form.get(f"{tag.name}"):
            new_post.tags.append(tag)

    db.session.add(new_post)
    db.session.commit()
    flash("Post created!", 'success')
    return redirect(f"/users/{id}")

@app.route('/posts/<int:id>')
def show_post(id):
    """ Page for post """
    post = Post.query.get_or_404(id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<int:id>/edit')
def show_edit_post(id):
    """ Page for showing edit post form """
    post = Post.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:id>/edit', methods=["POST"])
def edit_post(id):
    """ Page for editing post """
    post = Post.query.get_or_404(id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    post.tags.clear()

    tags = Tag.query.all()
    for tag in tags:
        if request.form.get(f"{tag.name}"):
            post.tags.append(tag)    

    db.session.commit()
    flash('Post successfully edited!', 'success')
    return redirect(f"/posts/{id}")

@app.route('/posts/<int:id>/delete', methods=["POST"])
def delete_post(id):
    """ Delete a post by id """
    post = Post.query.get_or_404(id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    flash("Post successfully deleted", 'success')
    return redirect(f"/users/{user_id}")

@app.route('/tags')
def show_tags():
    """ Display list of tags """

    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)

@app.route('/tags/<int:id>')
def show_tag_details(id):
    """ Display tag details """

    tag = Tag.query.get_or_404(id)
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def create_tag_form():
    """ Display form for creating new tag """

    posts = Post.query.all()
    return render_template('create_tag.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def create_tag():
    """ Create a new tag """ 

    name = request.form["tag_name"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    flash("New tag created!", 'success')
    return redirect('/tags')

@app.route('/tags/<int:id>/edit')
def edit_tag_form(id):
    """ Display Form for Editing Tag """

    tag = Tag.query.get_or_404(id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)

@app.route('/tags/<int:id>/edit', methods=["POST"])
def edit_tag(id):
    """ Edit a tag """
    tag = Tag.query.get_or_404(id)
    tag.name = request.form["tag_name"]
    db.session.commit()
    flash('Tag edited', 'success')
    return redirect(f"/tags/{id}")

@app.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    """ Delete a tag """

    tag = Tag.query.get_or_404(id)

    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted', 'success')
    return redirect('/tags')