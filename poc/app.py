from flask import Flask
from poc.db import init_db, get_db

app = Flask(__name__)

init_db(app)


@app.route('/')
def index():
    db = get_db()
    query = db.cursor().execute('SELECT 1')
    return query
