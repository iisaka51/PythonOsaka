from app import db
from app.models import User

user = User(username='python', email='python@example.com')
db.session.add(user)
#db.session.commit()
