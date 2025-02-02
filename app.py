from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from myaudio import printWAV
import time, random, threading
from turbo_flask import Turbo
#import Bcrypt
from flask_bcrypt import Bcrypt
from sqlalchemy import exc


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a5330bed949771bc9b0dc67e08b00274'
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
interval=10
FILE_NAME = "denzel.wav"
turbo = Turbo(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')
    
@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='Second Page', text='SEO TECH DEVELOPER second page')
  
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():   # checks if entries are valid
        try:
            pw_hash = bcrypt.generate_password_hash(form.password.data) #pulls the password's form
            print(pw_hash) #prints the password in hash format
        except ValueError:
            print('hashed password is empty')
        if bcrypt.check_password_hash(pw_hash, form.password.data):
            user = User(username=form.username.data, email=form.email.data, password = pw_hash)  
            db.session.add(user)
            try:
                db.session.commit()
            except exc.IntegrityError: #happens when you have same username twice
                print('can not have the same username')
            else:
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)
  
  
@app.route("/captions")
def captions():
    TITLE = "audio_file_name"
    return render_template('captions.html', songName=TITLE, file=FILE_NAME)
  

@app.before_first_request
def before_first_request():
    #resetting time stamp file to 0
    file = open("pos.txt","w") 
    file.write(str(0))
    file.close()

    #starting thread that will time updates
    threading.Thread(target=update_captions).start()

@app.context_processor
def inject_load():
    # getting previous time stamp
    file = open("pos.txt","r")
    pos = int(file.read())
    file.close()

    # writing next time stamp
    file = open("pos.txt","w")
    file.write(str(pos+interval))
    file.close()

    #returning captions
    return {'caption':printWAV(FILE_NAME, pos=pos, clip=interval)}

def update_captions():
    with app.app_context():
        while True:
            # timing thread waiting for the interval
            time.sleep(interval)

            # forcefully updating captionsPane with caption
            turbo.push(turbo.replace(render_template('captionsPane.html'), 'load'))

    
if __name__ == '__main__':
   app.run(debug=True)
  #app.run(debug=True, host="0.0.0.0")
#change to false since it the website may crash so it wont show any errors
