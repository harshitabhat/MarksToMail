import email
from tokenize import Name
from flask import Flask, render_template, request,flash,redirect
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "super secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class students(db.Model):
   Sno= db.Column(db.Integer, primary_key = True)
   Name = db.Column(db.String(100))
   Usn = db.Column(db.String(50))  
   Subject = db.Column(db.String(50))  
   Marks = db.Column(db.Integer)
   Mail_Id = db.Column(db.String(200))
  

   def __repr__(self):
        return f"{self.Sno} - {self.Name}"


mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'olduser95@gmail.com'
app.config['MAIL_PASSWORD'] = 'qawoxzhevdlcysmu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == "POST":
         email = request.form.get("email")
         password = request.form.get("password")
         if email=='anandbhat95@gmail.com' and password=='123':
            return render_template("marks.html")
         else:
            flash ("Invalid credentials")

    return render_template("index.html")

@app.route('/about')
def about():
     return render_template("about.html")

@app.route('/mtm',methods=['GET', 'POST'])
def mtm():
     if request.method == "POST":
      if request.form['submit_button'] == 'Send':
         # getting input with name = fname in HTML form
        name = request.form.get("name")
        usn = request.form.get("usn")
        # getting input with name = lname in HTML form
        email = request.form.get("email")
        sub = request.form.get("subject")
        marks = request.form.get("marks")
        mail_subject= 'Marks for '+sub
        msg = Message(
            mail_subject,
            sender ='olduser95@gmail.com',
            recipients = [email]
            )
        a= 'Good Luck \nThanks with Regards'
        msg.body =  " Hi "+name+" \n \nYour marks for "+sub+" is "+  marks +"\n \n \n "+a
        try:
            if len(name)>3 and len(sub)>2 and len(usn)>2 and len(str(marks))<4 and len(mail_subject)>4: 
               
                toto=students(Name=name.capitalize(),Usn=usn.upper(),Subject=sub.capitalize(),Marks=int(marks),Mail_Id=email)
                list_query=students.query.all()
                flag=False
                for result in list_query:
                 if name in result.Name or usn in result.Usn:
                    flag=True
                    break
                if flag:  
                    flash('details already exist')
                else:    
                    mail.send(msg)
                    db.session.add(toto)
                    db.session.commit()
                    flash ("Mail sent to "+ email)
            else:
                flash('Invalid details')    
        except:
            flash ("Please check entered details")
     return render_template("marks.html")

@app.route('/view',methods=['GET', 'POST'])
def view():
   los=students.query.all()
   return render_template("view_page.html",los=los)

@app.route('/search',methods=['GET', 'POST'])
def search():
    if request.method == "POST":
         search = request.form.get("search")
         l=students.query.filter_by(Usn=search).first_or_404(description='There is no data with {}'.format(search))
         print('\n',search)
         return render_template("search.html",l=l)
   
@app.route('/delete/<int:sno>')
def delete(sno):
    try:
        todo = students.query.filter_by(Sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/view")
    except:
        return '<h1 align="center">Someting went wrong in DB</h1> '    

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        usn = request.form['usn']
        sub = request.form['subject']
        marks = request.form['marks']
        mail = request.form['mail']
        todo = students.query.filter_by(Sno=sno).first()
        todo.Name = title.capitalize()
        todo.Usn = usn.upper()
        todo.Subject = sub.capitalize()
        todo.Marks = int(marks)
        todo.Mail_Id = mail
        if len(title)>3 and len(sub)>4 and len(usn)>4 and len(str(marks))<4 and len(mail)>4:
            db.session.add(todo)
            db.session.commit()
            return redirect("/view")
        else:
            flash ("Please check entered details")   
        
    todo = students.query.filter_by(Sno=sno).first()
    return render_template('updates.html', todo=todo)

if __name__ == '__main__':
   app.run(debug = True)