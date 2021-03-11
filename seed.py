from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

user1 = User(first_name='Alan', last_name='Alda')
user2 = User(first_name='Joel', last_name='Burton', image_url='http://joelburton.com/joel-burton.jpg')
user3 = User(first_name='Jane', last_name='Smith')

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()