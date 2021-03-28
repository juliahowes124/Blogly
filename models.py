import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    """ Model for User """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String(), default="https://winaero.com/blog/wp-content/uploads/2015/05/windows-10-user-account-login-icon.png")

    posts = db.relationship('Post',  cascade="all, delete")

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def find_user_id(cls, first, last):
        return cls.query.filter(User.first_name == first, User.last_name == last).first()

  
class Post(db.Model):
    """ Model for Post """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)

    title = db.Column(db.String(50), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User')

    tags = db.relationship('Tag', secondary='post_tags')

    @property
    def friendly_date(self):
        return self.created_at.date()

class Tag(db.Model):
    """ Model for Tag """

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
    
    name = db.Column(db.String(50), unique=True, nullable=False)

    posts = db.relationship('Post', secondary='post_tags')

class PostTag(db.Model):
    """ Model for Post Tag """

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True, nullable=False) 
    
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True, nullable=False)
    