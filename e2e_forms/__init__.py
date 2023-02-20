from flask import Flask, request,g 
from markupsafe import escape
import sqlite3
app = Flask(__name__)
from .db import query_db




from .db import get_db
@app.route('/')
def hello():
    for user in query_db('select * from users'):
        print(user)
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

