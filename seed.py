from models import User, Post, Tag, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

user1 = User(first_name='Alan', last_name='Alda')
user2 = User(first_name='Joel', last_name='Burton', image_url='http://joelburton.com/joel-burton.jpg')
user3 = User(first_name='Jane', last_name='Smith')

post_alan1 = Post(title="Hello", content="My name is Alan Alda", author_id=1)
post_alan2 = Post(title="I am an actor", content="I was in M*A*S*H, which is an old show", author_id=1)
post_joel = Post(title="Introduction to Typescript", content="Typescript is like Javascript", author_id=2)

tag1 = Tag(name="fun")
tag2 = Tag(name="Even More")
tag3 = Tag(name="Bloop")


db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.add(post_alan1)
db.session.add(post_alan2)
db.session.add(post_joel)

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

db.session.commit()