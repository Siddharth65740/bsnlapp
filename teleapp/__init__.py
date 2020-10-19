from flask import Flask

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_datepicker import datepicker

app =  Flask(__name__)
db=SQLAlchemy(app)
ma=Marshmallow(app)


app.config['SECRET_KEY']='1234'
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:123@localhost:5432/master"


app.config['MAIL_SERVER']="smtp.googlemail.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']='True'
app.config['MAIL_USERNAME']='dgmcmgujarat@gmail.com'
app.config['MAIL_PASSWORD']='Sanjay@123'
mail=Mail(app)

datepicker=datepicker(app)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

login_manager=LoginManager(app)
login_manager.login_view="Login"
login_manager.login_message_category="info"

from teleapp import routes