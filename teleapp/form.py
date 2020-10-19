from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,validators,PasswordField,SubmitField,ValidationError,IntegerField,BooleanField,TextAreaField,DateTimeField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileField,FileAllowed
from teleapp.model import Fieldofficer,ssa
from flask_login import current_user
from wtforms.fields.html5 import DateField

# --  1 ---------Login Form ---------
class LoginForm(FlaskForm):
    hr_no = IntegerField('HR Number :', validators=[DataRequired()])
    #email = StringField('Email :',validators=[DataRequired(),Email()])
    password = PasswordField("Password :",validators=[DataRequired(),Length(min=2,max=10)])
    remember_me=BooleanField("Remember Me")
    login = SubmitField('Login In')

#---------Registration Form ---------
class RegisterForm(FlaskForm):
    hr_no = StringField('HR Number:',validators=[DataRequired()])
    mob_no = StringField('Mobile Number :', validators=[DataRequired(),Length(min=10,max=10)])
    ssaname=SelectField('SSA: ',choices=[(str(ssa.id),ssa.ssaname) for ssa in ssa.query.all()])
    picture_profile = FileField("Upload profile picture ", validators=[FileAllowed(["jpg", "png"])])
    email = StringField('Email :',validators=[DataRequired(),Email()])
    password = PasswordField("Password :",validators=[DataRequired(),Length(min=2,max=10)])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), Length(min=2, max=10),EqualTo("password")])
    name=StringField("User Name ")
    signup = SubmitField('Sign Up')


    def validate_email(self,email):
        user=Fieldofficer.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError('Email is already taken  choose another one . ')

    def validate_hr_no(self,hr_no):
        user = Fieldofficer.query.filter_by(hr_no=hr_no.data).first()
        if user:
            raise ValidationError('User No  is already taken  choose another one . ')
#---------Account Form ---------
class AccountForm(FlaskForm):
    hr_no = IntegerField('HR Number:', validators=[DataRequired()])
    email = StringField('Email :', validators=[DataRequired(), Email()])
    name = StringField("User Name ")
    picture_profile=FileField("Upload profile picture ",validators=[FileAllowed(["jpg","png"])])
    update = SubmitField('Update')

    def validate_email(self, email):
        if current_user.email != email.data :
            user = Fieldofficer.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already taken  choose another one . ')

    def validate_hr_no(self, hr_no):
        if current_user.hr_no != hr_no.data :
            user = Fieldofficer.query.filter_by(hr_no=hr_no.data).first()
            if user:
                raise ValidationError('User No  is already taken  choose another one . ')


#---------Faultlog Form ---------
class PostForm(FlaskForm):
    btsname=StringField("BTS Name :",validators=[DataRequired()])
    nb_of_tsps=StringField("Number of TSP's :",validators=[DataRequired()])
    reason=TextAreaField("Reason :")

    submit = SubmitField('Save')

#---------MNP Form ---------
class MNPForm(FlaskForm):
    pocnt=IntegerField("Port-out Count :",validators=[DataRequired()])
    picnt=IntegerField("Port-in Count :",validators=[DataRequired()])
    popidt=DateField("Date:")
    submit = SubmitField('Save')

#---------Entry Form ---------
class EntryForm(FlaskForm):
    fname=StringField("Fname:")
    lname=StringField("Lname:")
    email=StringField("email:")
    pswd1=StringField("PSWD1 :",validators=[DataRequired()])
    pswd2=StringField("PSWD2:",validators=[DataRequired()])
    submit=SubmitField('Save')

#---------Upload Form ---------
class UploadForm(FlaskForm):
    desc=StringField("Enter Desc :",validators=[DataRequired()])
    uploaddt = DateField("Upload Date ")
    docu=FileField("Upload profile picture ",validators=[FileAllowed(["jpg", "png","pdf","xlsx"])])
    submit = SubmitField('Save')

#---------Import Form ---------
class ImportForm(FlaskForm):
    docu=FileField("Import CSV File... ",validators=[FileAllowed(["csv"])])
    submit = SubmitField('Save')

