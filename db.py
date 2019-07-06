from flask_sqlalchemy import SQLAlchemy

from .app import app

POSTGRES_URL = 'dumbo.db.elephantsql.com:5432'
POSTGRES_DB = 'vziectjf'
POSTGRES_USER = 'vziectjf'
POSTGRES_PW = 'Tjn8kLJho38COoPfhjcqAIxAybExNCwz'

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=POSTGRES_USER,
    pw=POSTGRES_PW,
    url=POSTGRES_URL,
    db=POSTGRES_DB
)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
