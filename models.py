from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.sql import func
# from flask_wtf import Form 
#from wtforms import StringField, BooleanField
#from wtforms.validators import DataRequired
db = SQLAlchemy()


# the model schema for the database
class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feed = db.Column(db.String(100), nullable=False)
    amount_entered = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)
    date_added =  db.Column(db.DateTime, default= datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)

    
# revised class Reccipe is for calulating using coop details 
class FeedRecipe(db.Model):
    __tablename__ = 'feedrecipe'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feed = db.Column(db.String(100), nullable=False)
    days = db.Column(db.Integer, nullable=False)
    total_feed = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    
    #Kondwani - make calculations nased on specific coop chosen
    #Kondwani - update user profile, delete coop
    #for cost and amount for individual ingredients, make result downloadable
    
    date_added =  db.Column(db.DateTime, default= datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
    coop_id = db.Column(db.Integer,
                        db.ForeignKey('coops.id', ondelete='CASCADE'),
                        nullable=False)
# 
# from flask_wtf import FlaskForm
# from wtforms import StringField
# from wtforms.validators import DataRequired
# 
# class MyForm(FlaskForm):
#     name = StringField('name', validators=[DataRequired()])

# class Ingredients(db.Model) #ingredients for demo to be managed by admin
#     __tablename__='ingredients'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ing_a = db.Column(db.String(100), nullable=False)
#     ing_b = db.Column(db.String(100), nullable=False)
#     ing_c = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Integer(), nullable=False)
#     
#     
# class Feed(db.Column)
#     __tablename__='feed'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     days = db.Column(db.Integer(), nullable=False)
#     total_consumption= db.Column(db.Integer(), nullable=False)
#     total_cost = db.Column(db.Integer(), nullable=False)
#    coop_id = db.Column(db.Integer,
#    db.ForeignKey('coops.id', ondedelete='CASCADE'),
            #  nullable=False)
#
#
class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    date_added =  db.Column(db.DateTime, default= datetime.now)
    phone = db.Column(db.Integer(), nullable=False)
#     image = db.Column(LargeBinary, nullable = True)
#    
    recipe_object = db.relationship('Recipe', backref='users', lazy=True, uselist=True,
                                    cascade="all,delete")
    
    coops_object = db.relationship('Coops', backref='users', lazy=True, uselist=True,
                                     cascade="all,delete")

    #class UsersForm(FlaskForm): for form validation and etc
        
class Coops(db.Model):
    __tablename__= 'coops'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    date_added =  db.Column(db.DateTime, default= datetime.now)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.id', ondelete='CASCADE'),
                        nullable=False)
 
    
    #date
    
   #age= (date_added-current_date)/7 + age
class Tips(db.Model):
    __tablename__='tips'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(100))
    date_added =  db.Column(db.DateTime, default= datetime.now)
    
    

  
