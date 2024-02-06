import datetime
import uuid
from functools import wraps

import jwt
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config['SECRET_KEY']='c59aafab4601e96d7df78253d59efb1e'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
db = SQLAlchemy(app)

app.app_context().push()

#TODO: dividir en subcarpetas
class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   public_id = db.Column(db.Integer)
   name = db.Column(db.String(50))
   password = db.Column(db.String(50))
   admin = db.Column(db.Boolean)
   
class Books(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   name = db.Column(db.String(50), unique=True, nullable=False)
   Author = db.Column(db.String(50), unique=True, nullable=False)
   Publisher = db.Column(db.String(50), nullable=False)
   book_prize = db.Column(db.Integer)
   

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
      token = None
      if 'x-access-tokens' in request.headers:
          token = request.headers['x-access-tokens']

      if not token:
          return jsonify({'message': 'a valid token is missing'})
      try:
         data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
         current_user = Users.query.filter_by(public_id=data['public_id']).first()
      except Exception:
         return jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)

   return decorator

@app.route('/register', methods=['POST'])
def signup_user(): 
   data = request.get_json() 
   hashed_password = generate_password_hash(data['password'], method='sha256')
 
   new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
   db.session.add(new_user) 
   db.session.commit()   
   return jsonify({'message': 'registered successfully'})