from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

SECRET = '8c135d24ed30d57f770967295653cc48adf3003ceedc95be'

app = FastAPI()
manager = LoginManager(SECRET, tokenUrl='/auth/token')

fake_db = {'freddie@example.com': {'password': 'queen'}}
@manager.user_loader
def load_user(email: str):
    user = fake_db.get(email)
    return user

@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get('/')
def index(user=Depends(manager)):
    return {"Hello": "World!"}
