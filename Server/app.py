import os
import sys
from flask import Flask, request
from flask_orator import Orator, jsonify
from orator.orm import belongs_to, has_many, belongs_to_many
import graphlab

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

  @belongs_to_many('subscribes','subscriber_id','subscribed_id')
  def blogs(self):
    return Blog

  def is_subscribing(self, blog):
            return self.blogs().where('subscribed_id', blog.id).exists()

  def subscribes(self,blog):
    if not self.is_subscribing(blog):
      self.blogs().attach(blog)


class Blog(db.Model):
  __fillable__ = ['url']
  __table__ = 'blogs'

  @belongs_to_many(
       'subscribes',
       'subscribed_id', 'subscriber_id'
  )
  def subscribers(self):
        return User

  @has_many
  def pages(self):
    return Page

class Subscribe(db.Model):
  __fillable__=['subscribed_id','subscriber_id']
  __table__ = 'subscribes'

class Page(db.Model):
  __fillable__ = ['pageUrl']
  @belongs_to
  def blogs(self):
    return Blog 

class Recommender():
  def __init__(self):
    graphlab.product_key.set_product_key('D75B-9AD5-8257-3E33-E7B3-E7E6-EE34-7D86')
    users = User.all()
    userIds = []
    blogIds = []
    for user in users :
      blogs = user.blogs
      for blog in blogs :
        userIds.append(user.id)
        blogIds.append(blog.id)

    self.sf = graphlab.SFrame({'user_id':userIds,'item_id':blogIds})
    self.recommender = graphlab.recommender.create(self.sf)

  def append (self, userId, blogIds) :
    sf = graphlab.SFrame({'user_id':[userId]*len(blogIds),'item_id':blogIds})
    self.sf.append(sf)
    self.recommender = graphlab.recommender.create(self.sf)

  def recommend(self,userId) :
    return self.recommender([userId])

recommender = Recommender()
    

@app.route('/users', methods=['POST'])
def create_user():
  global recommender
  params=  request.get_json()
  _accessToken = params['accessToken']
  _email = params['email']
  user = User.first_or_create(accessToken=_accessToken,email=_email)
  blogs = params['blogs']

  for burl in blogs:
    blog = Blog.first_or_create(url=burl)
    user.subscribes(blog)
  
  return jsonify(user)

@app.route('/users/<int:user_id>/recommend', methods=['GET'])
def get_user_recommend(user_id):
  user = User.find_or_fail(user_id)
  newBlogs = []

  for burl in blogs:
    blog = Blog.first_or_create(url=burl)
    sub = Subscribe.where("subscribed_id",blog.id).where("subscriber_id",user.id).get()
    if (sub == None) :
      user.subscribes(blog)
      newBlogs.append(blog.id)

  recommender.append(user.id,newBlogs)

  return jsonify(user)


@app.route('/users/<int:user_id>/recommend', methods=['GET'])
def get_user_recommend(user_id):
  global recommender
  user = User.find_or_fail(user_id)
  #TODO(seralee)
  return jsonify(recommender.recommend(user_id))


if __name__ == '__main__':
  app.run()
