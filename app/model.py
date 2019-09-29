from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Places(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lat = db.Column(db.String)
    lon = db.Column(db.String)
    address = db.Column(db.String)
    rating = db.Column(db.Float)