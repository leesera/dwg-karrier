import os
from flask import Flask, request
from flask_orator import Orator, jsonify
from orator.orm import belongs_to, has_many

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

  @has_many
  def messages(self):
    return Message


class Blog(db.Model):

    __fillable__ = ['url']

    @belongs_to
    def user(self):
        return User

@app.route('/users', methods=['POST'])
def create_user():
  user = User.create(**request.get_json())

  return jsonify(user)

if __name__ == '__main__':
    app.run()
