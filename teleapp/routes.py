from flask import render_template,flash,redirect,url_for,request,jsonify
from teleapp import db,app,bcrypt,mail,datepicker
from teleapp.form import  RegisterForm,LoginForm,AccountForm,PostForm,MNPForm,UploadForm,ImportForm,EntryForm
from teleapp.model import Fieldofficer,Faultlog,mnp_popi,Letters,FaultSchema,ssaSchema,myform
from flask_login import login_user,current_user,logout_user,login_required
import secrets,math,cmath
import os
import sys
import psycopg2
from PIL import Image
import requests

con = None
f = None
con = psycopg2.connect(database='master', user='postgres',password='123')

from flask_mail import Message
# 0 ----------- Routes for Dashboard -----------------
@app.route("/Dashboard",methods=['GET','POST'])
def Dashboard():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template("index.html")


@app.route("/sample_form")
def sample_form():
     form = EntryForm()
     return render_template("sample_form.html",form=form)

@app.route("/my_chart",methods = ['GET','POST'])
def my_chart():
    faults = Faultlog.query.all();
    return render_template("Chart_sample.html", posts=faults)

@app.route("/my_chartdata",methods = ['GET'])
def my_chartdata():
    f=Faultlog.query.with_entities(Faultlog.nb_of_tsps,Faultlog.btsname).all();

    values=[]
    labels=[]
    dataset=[];
    for row in f :
        print(row);
        values.append(int(row[0]))
        labels.append(row[1][:4])

    #fault_schema=FaultSchema(many=True);

    #output=fault_schema.dump(f)
    #print(output);
    return jsonify({"data":values[:6],"labels":labels[:6],"dataset":dataset});



@app.route("/my_barchart", methods=['GET'])
def my_barchart():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    # f=Faultlog.query.with_entities(Faultlog.nb_of_tsps).all();
    # values=[]
    # for row in f :
    #     print(row);
    #     values.append(int(row[0]*100))
    return jsonify({"data":values,"labels":labels});

    return render_template('Chart_sample.html', values=values, labels=labels, legend=legend)


@app.route("/dashboard")
def dashboard():
     return render_template("index.html")

@app.route("/my_form",methods = ['GET','POST'])
def my_form():
    form = EntryForm()
    if form.validate_on_submit():
        entry_data = myform(fname=form.fname.data, lname=form.lname.data, email=form.email.data,pswd1=form.pswd1.data,pswd2=form.pswd2.data)
        print(form.fname.data);
        db.session.add(entry_data);
        db.session.commit();
        flash("New Record Added..", "info")
        return redirect(url_for("popi_report"))
        # return render_template("MNPReport.html",form=form)

    return render_template("auth-register.html", form=form)




@app.route("/datatable")
def datatables():
    faults = Faultlog.query.all();
    return render_template("export_table.html",posts=faults)

# RETURN ALL DATABASE POST RECOREDS
@app.route("/fault_list")
def faultlist():
    fault = Faultlog.query.all();
    fault_schema=FaultSchema(many=True);
    output=fault_schema.dump(fault)
    return jsonify({"data":output});


@app.route("/bts_count")
def bts_count():
    fault = Faultlog.query.filter_by(nb_of_tsps="2").count();
    print(fault);
    #fault_schema=FaultSchema();
    #output=fault_schema.dump(fault)
    return jsonify({"data":fault});



# ----------- Routes for home -----------------
@app.route("/")
@app.route("/home")
def home():
   page = request.args.get('page',1,type=int)
  # results=db.session.execute("select * from Faultlog");

   posts = Faultlog.query.paginate(page=page,per_page=2)
   return render_template("HomePage.html",posts=posts)


# --  1 ----------- Routes for Login -----------------
@app.route("/Login",methods=['GET','POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Fieldofficer.query.filter_by(hr_no = form.hr_no.data).first()

        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)

            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            flash("You are successfully logged in!!!", "success")

            return redirect(url_for('home'))
        else:
            flash("Invalid HR Number ... ", "danger")
    return render_template('index.html', title='Login', form=form)



# ----------- Routes for Register -----------------

@app.route("/Register",methods = ['GET','POST'])
def Register():
    if current_user.is_authenticated :
         return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit() :
            hash_password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            picture_name=save(form.picture_profile.data)
            user=Fieldofficer(hr_no=form.hr_no.data,email=form.email.data,password=hash_password,name=form.name.data,profile_picture = picture_name,ssa=form.ssaname.data)
            db.session.add(user)
            db.session.commit()
            flash('Your Account is created login now ','success')

            #image_name = url_for('static', filename='profile_pics/' + user.profie_picture);
            #return render_template("Accounts.html", title="Account", image_name=image_name, form=form)
            return redirect(url_for('Login'))
    return render_template('Register.html',title='Register', form=form)

def save(form_picture):
    hash_name=secrets.token_hex(8);
    file_name,ext=os.path.splitext(form_picture.filename)
    print("filename :",file_name,"  ext:",ext)
    picture_path=os.path.join(app.root_path,"static/profile_pics/",hash_name+ext)
    output_size=(125,125)
    comp_image=Image.open(form_picture)
    comp_image.thumbnail(output_size)

    comp_image.save(picture_path)
    return hash_name+ext;

# ----------- Routes for Account -----------------

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=AccountForm()
    if form.validate_on_submit():
        #print(form.picture_profile.data.filename)
        if form.picture_profile.data :
            image_name=save(form.picture_profile.data)
            current_user.profie_picture = image_name

        print("new file name:",image_name)
        current_user.hr_no=form.hr_no.data
        current_user.email=form.email.data
        current_user.name=form.name.data
        db.session.commit();
        flash("your account has been updated ","success")
        return redirect(url_for("account"))
    form.hr_no.data=current_user.hr_no
    form.email.data=current_user.email
    form.name.data=current_user.name
    image_name=url_for('static',filename='profile_pics/'+ current_user.profile_picture);
    return  render_template("accounts.html",title="Account",image_name=image_name,form=form)

# ----------- Routes for Logout -----------------
@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for('Login'))
# ----------- Routes for /faultlog/new -----------------
@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
         print(form.btsname.data)
         new_post=Faultlog(btsname=form.btsname.data,nb_of_tsps=form.nb_of_tsps.data,reason=form.reason.data,incharge=current_user)

         db.session.add(new_post);
         db.session.commit();
         flash("New Fault is booked..","info")
         return redirect(url_for("home"))
    posts = Faultlog.query.all();
    return render_template("faultlog.html",form=form,posts=posts)

# ----------- Routes for /faultlog/update -----------------
@app.route("/post/update/<post_id>",methods=['GET','POST'])
@login_required
def update_post(post_id):
    form=PostForm()
    post = Faultlog.query.get(post_id);
    if form.validate_on_submit():
          post.btsname=form.btsname.data
          post.nb_of_tsps = form.nb_of_tsps.data
          post.reason=form.reason.data
          db.session.commit()
          flash("Post has been updated ","success")
          return redirect(url_for("home"))

    form.btsname.data=post.btsname
    form.nb_of_tsps.data=post.nb_of_tsps
    form.reason.data=post.*reason
    return render_template("faultlog.html",form=form,post=post)

# ----------- Routes for /faultlog/delete -----------------
@app.route("/post/delete/<post_id>",methods=['GET','POST'])
@login_required
def delete_post(post_id):
    form=PostForm()
    post = Faultlog.query.get(post_id);
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))



@app.route("/post/view/<userid>",methods=['GET','POST'])
def user_post_view(userid):

     user=Fieldofficer.query.get(userid);
     posts=user.faultlogs

     return render_template("Faultview.html",userid=userid, posts=posts)

@app.route("/post/mail/<id>",methods=['GET','POST'])
def send_email(id):
        user = Fieldofficer.query.get(id);
        posts = user.faultlogs
    #try:
        msg = Message('Dear Siidharth,your result for sem-1', sender='dgmcmgujarat@gmail.com', recipients=['dgmcmgujarat@gmail.com'])
        message="reports \n ";
        for post in posts:
            message=message+ f'''
                \n Your following BTS are Down:
                    {post.btsname}
                    {post.reason} 
                   '''
        print("message :",message)
        msg.body=message
        print("message bind in a body");
        mail.send(msg)
        print('Mail has been sent')
   # except Exception :
    #    print("error in send_email")

        return redirect(url_for('home'))


# ----------- Routes for /mnp/entry -----------------
@app.route("/mnp/entry",methods=['GET','POST'])
@login_required
def mnp_entry():
    form=MNPForm()
    if form.validate_on_submit():

         mnp_data= mnp_popi(pocnt=form.pocnt.data,picnt=form.picnt.data,popidt=form.popidt.data)

         db.session.add(mnp_data);
         db.session.commit();
         flash("New Record Added..","info")
         return redirect(url_for("popi_report"))
         #return render_template("MNPReport.html",form=form)
    posts = mnp_popi.query.all();
    return render_template("mnpdataentry.html",form=form,posts=posts)

# ----------- Routes for /mnp/popireport -----------------
@app.route("/mnp/popireport")
def popi_report():
   sql = ("select 'TOTAL' as ssa,sum(pocnt) as TOTPOCNT,sum(picnt) as TOTPICNT from mnp_popi "
          "union all "
          "select popidt::text as ssa,pocnt,picnt from mnp_popi"
          )

   results = db.session.execute(sql);
   #posts = mnp_popi.query.all()
   return render_template("MNPReport.html",posts=results)

# ----------- Routes for /uploaddoc -----------------
@app.route("/uploaddoc",methods=['GET','POST'])
def upload_doc():
   form=UploadForm()
   if form.validate_on_submit():
       filename = save(form.docu.data)

       print(filename)
       doc = Letters(desc=form.desc.data, uploaddt=form.uploaddt.data, docu=filename)

       db.session.add(doc);
       db.session.commit();
       flash("New Letter uploaded..", "info")
       return redirect(url_for("tocorp"))

   return render_template("UploadForm.html", form=form)
def save(fname):
    hash_name=secrets.token_hex(8);
    file_name,ext=os.path.splitext(fname.filename)
    print("filename :",file_name,"  ext:",ext)
    picture_path=os.path.join(app.root_path,"static/to_corp_letters/",hash_name+ext)
    #output_size=(125,125)
    #comp_image= Image.open(fname)
    #comp_image.thumbnail(output_size)

    fname.save(picture_path)
    return hash_name+ext;


# ----------- Routes for /download -----------------
@app.route("/download")
def tocorp():
    posts = Letters.query.all();
    return render_template("view_letters.html",posts=posts)

# #----------- Routes for Import CSV files ---------
# @app.route("/import")
# def csv_import():
#     f = open('D:/testingsheet.csv', 'r')
#     cur = con.cursor()
#     cur.copy_from(f,"mnp_popi", columns=('pocnt', 'picnt','popidt'), sep=",")
#     con.commit()
#
#     return render_template("error_page.html",msg="Data Imported..")

# ----------- Routes for /Import -----------------
@app.route("/import",methods=['GET','POST'])
def import_doc():
   form=ImportForm()
   if form.validate_on_submit():
       f = extract(form.docu.data)
       print(f)
       f = open('D:\\' +f , 'r')
       cur = con.cursor()
       cur.copy_from(f, "mnp_popi", columns=('pocnt', 'picnt', 'popidt'), sep=",")
       con.commit()
       flash('Data Imported Successfully.. ', 'success')

   return render_template("ImportForm.html",form=form)

def extract(fname):
    file_name,ext=os.path.splitext(fname.filename)
    return file_name+ext

@app.route("/table")
def tables():
     return render_template("export-table.html")







