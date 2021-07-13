from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a5330bed949771bc9b0dc67e08b00274'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

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
    if form.validate_on_submit(): # checks if entries are valid
      user = User(username=form.username.data, email=form.email.data, password=form.password.data)
      db.session.add(user)
      db.session.commit()
      flash(f'Account created for {form.username.data}!', 'success')
      return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)
  
  
@app.route("/captions")
def captions():
    TITLE = "audio_file_name"
    FILE_NAME = "examples_english.wav"
    return render_template('captions.html', songName=TITLE, file=FILE_NAME)

    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
