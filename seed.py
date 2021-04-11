from models import User, Post, Tag, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

user1 = User(first_name='Julia', last_name='Howes', image_url='https://juliahowes.com/images/profile-pic.png')
user2 = User(first_name='Mr.', last_name='Cat', image_url="https://images.squarespace-cdn.com/content/v1/53a0ded4e4b0514810c15d4b/1403054697994-IBF0BXUSD3JP3VH07YTS/ke17ZwdGBToddI8pDm48kE8bApAffW_Dpq7WPVz5gAZZw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVHMHqM9QIeHMgTC2SVmrLQsZlmG0EqsTmZgl3AyoD3WsWvZ84NDtP7Anw8h90Oqwxk/rainbow-cat.jpg")
user3 = User(first_name='John', last_name='Doe')

post_julia1 = Post(title="Howdy", content="Hi, my name is Julia!", author_id=1)
post_julia2 = Post(title="Which coding bootcamp should you choose?", content="Rithm School of course!", author_id=1)
post_cat = Post(title="Meow", content="Meow, meow meow meow. Meow meow meow meow meow, meow meow meow meow. Meow!", author_id=2)

tag1 = Tag(name="Fun")
tag2 = Tag(name="Informational")
tag3 = Tag(name="Bloop")


db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.add(post_julia1)
db.session.add(post_julia2)
db.session.add(post_cat)

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

db.session.commit()