from teleapp import db
from datetime import datetime
from teleapp import ma
from teleapp import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Fieldofficer.query.get(id)

#----------Fieldofficer db-------------------

class Fieldofficer(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    hr_no=db.Column(db.Integer,nullable=False,unique=True)
    ssa = db.Column(db.String(30), nullable=False, unique=True)
    email=db.Column(db.String(120),nullable=False,unique=True)
    password=db.Column(db.String(200),nullable=False)
    name=db.Column(db.String(30))
    profile_picture=db.Column(db.String(100),nullable=True,default="default.jpg")
    faultlogs = db.relationship("Faultlog",backref="incharge",lazy=True)

    def __repr__(self):
        return f"Fieldofficer('{self.email}','{self.hr_no}','{self.name}'"

#----------Faultlog db-------------------

class Faultlog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    btsname=db.Column(db.String(20),nullable=False)
    nb_of_tsps=db.Column(db.Integer, nullable=False)
    reason=db.Column(db.String(300),nullable=False)
    downdatetime=db.Column(db.Date,nullable=False,default=datetime.utcnow)
    updatetime=db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('fieldofficer.id'),nullable=False)

    def __repr__(self):
        return f"Faultlog('{self.btsname}','{self.reason}','{self.downdatetime}')"
#----------MNP Po/Pi Data db-------------------

class mnp_popi(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    pocnt=db.Column(db.Integer,nullable=False)
    picnt=db.Column(db.Integer, nullable=False)
    popidt=db.Column(db.Date,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"mnp_popi('{self.pocnt}','{self.picnt}','{self.popidt}')"


#----------SSA db-------------------
class ssa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssaname = db.Column(db.String(30), nullable=False, unique=True)
    def __repr__(self):
        return f"SSA('{self.ssaname}')"

#----------Letters-------------------
class Letters(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    desc=db.Column(db.String(200),nullable=False,unique=True)
    uploaddt=db.Column(db.Date, nullable=False, default=datetime.utcnow)
    docu=db.Column(db.String(100),nullable=True)

    def __repr__(self):
        return f"Letters('{self.desc}','{self.uploaddt}','{self.docu}'"

#----------My Form-------------------
class myform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname=db.Column(db.String(200))
    lname=db.Column(db.String(200))
    email = db.Column(db.String(120), nullable=False, unique=True)
    pswd1 = db.Column(db.String(200), nullable=False)
    pswd2 = db.Column(db.String(200), nullable=False)


class ssaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ssa;

class FaultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Faultlog;