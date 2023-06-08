from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "cc26e0e3b4e801f72935eaeef2a599dc"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaccine.db'
db = SQLAlchemy(app)

from app import router
