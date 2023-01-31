from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from secret import secret
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = secret

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

base = 'http://127.0.0.1:5000/'

#database model
class Url(db.Model):
    id_ = db.Column('url_id', db.Integer, primary_key = True)
    original_url = db.Column("Original_URL",db.String(250))
    short_url = db.Column("Short_URL",db.String(50))

    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url

#create the short_url
def create_short_url():
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' 
    while True:
        rand = random.choices(characters, k=5) #creating a random 5 character string
        rand = base + ''.join(rand) #adding the 5 character string to base
        exists_short = Url.query.filter_by(short_url=rand).first()
        if not exists_short:
            return rand  #returning short_url back


#main page
@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        ori_url = request.form['ori_url']
        exists = Url.query.filter_by(original_url=ori_url).first()

        if exists:
            get_short_url = Url.query.filter_by(original_url=ori_url).first()
            return render_template('home.html',short_url=get_short_url.short_url)
        else:
            short_url = create_short_url()  #getting rand from create_short_url()
            print(short_url)
            new_url = Url(ori_url,short_url)  #inserting new data into database
            db.session.add(new_url)
            db.session.commit()
            return render_template('home.html',short_url=short_url) #returning short_url to frontend
    else:
        return render_template('home.html') #if request not made, return only home.html

#redirect logic
@app.route('/<short>')
def redirect_url(short):
    get_original_url = Url.query.filter_by(short_url=base+short).first()
    url = str(get_original_url.original_url)
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True)