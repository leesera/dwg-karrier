import os
from flask import Flask, request
from flask_orator import Orator, jsonify
from orator.orm import belongs_to, has_many, belongs_to_many

# Configuration
DEBUG = True
ORATOR_DATABASES = {
    'default': 'roys',
    'roys': {
        'driver': 'sqlite',
        'database': os.path.join(os.path.dirname(__file__), 'roys.db')
    }
}

# Creating Flask application
app = Flask(__name__)
app.config.from_object(__name__)

# Initializing Orator
db = Orator(app)

class User(db.Model):

  __fillable__ = ['accessToken', 'email']
  __table__ = 'users'

  @belongs_to_many(
       'subscribes',
       'subscriber_id', 'subscribed_id',
       with_timestamps=True
  )
  def subscribes(self):
        return Blog


class Blog(db.Model):
  __fillable__ = ['url']

  @belongs_to_many(
       'subscribers',
       'subscribed_id', 'subscriber_id',
       with_timestamps=True
  )
  def subscribers(self):
        return User

  @has_many
  def pages(self):
    return Page


class Page(db.Model):
  __fillable__ = ['pageUrl']
  @belongs_to
  def blogs(self):
    return Blog 

@app.route('/users', methods=['POST'])
def create_user():
  user = User.create(**request.get_json())

  return jsonify(user)


@app.route('/users/<int:user_id>/recommend', methods=['GET'])
def get_user_messages(user_id):
  user = User.find_or_fail(user_id)
  find_recommend(user)
  
  return None 


if __name__ == '__main__':
  app.run()
