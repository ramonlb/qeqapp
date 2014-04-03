from app import app
from flask import g
import sqlite3 as lite

DATABASE = 'app/db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = lite.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

