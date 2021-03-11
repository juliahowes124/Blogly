from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String(), default="https://winaero.com/blog/wp-content/uploads/2015/05/windows-10-user-account-login-icon.png")

    @classmethod
    def find_user_id(cls, first, last):
        return cls.query.filter(User.first_name == first, User.last_name == last).first().id
    
