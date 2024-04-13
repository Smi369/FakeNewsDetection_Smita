import os
import MySQLdb
import smtplib
import random
import string
from datetime import datetime
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash, send_file
from database import db_connect,aa_log,owner_reg,owner_login,vu1,vu3,predict_act,vn1,van2,vu5
from database import db_connect
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords')
# from cloud import uploadFile,downloadFile,close

from sendmail import sendmail


# def db_connect():
#     _conn = MySQLdb.connect(host="localhost", user="root",
#                             passwd="root", db="assigndb")
#     c = _conn.cursor()

#     return c, _conn


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def FUN_root():
    return render_template("index.html")
    
@app.route("/admin.html")
def admin():
    return render_template("admin.html")

@app.route("/an.html")
def an():
    return render_template("an.html")

@app.route("/user.html")
def user():
    return render_template("user.html")

@app.route("/reg.html")
def reg():
    return render_template("reg.html")

@app.route("/ahome.html")
def ahome():
    return render_template("ahome.html")

@app.route("/uhome.html")
def uhome():
    return render_template("uhome.html")

@app.route("/index")
def index():
    return render_template("index.html") 

@app.route("/vu.html")
def vu():
    data = vu1()
    print(data)
    return render_template("vu.html",data = data)

@app.route("/vn.html")
def vn():
    data = vn1()
    print(data)
    return render_template("vn.html",data = data)

@app.route("/van.html")
def van():
    data = van2()
    print(data)
    return render_template("van.html",data = data)


@app.route("/vu2", methods = ['GET','POST'])
def vu2():
    b = request.args.get('b')
    d = request.args.get('d')
    vu3(b,d)
    return render_template("ahome.html")

@app.route("/vu4", methods = ['GET','POST'])
def vu4():
    b = request.args.get('b')
    d = request.args.get('d')
    vu5(b,d)
    return render_template("ahome.html")




@app.route("/alogin", methods=['GET', 'POST'])       
def alogin():
    if request.method == 'POST':
        status = aa_log(request.form['username'], request.form['password'])
        print(status)
        if status == 1:
            session['username'] = request.form['username']
            return render_template("ahome.html", m1="sucess")
        else:
            return render_template("admin.html", m1="Login Failed")
        

@app.route("/oregact", methods = ['GET','POST'])
def oregact():
   if request.method == 'POST':    
      
      status = owner_reg(request.form['username'],request.form['password'],request.form['email'],request.form['mobile'],request.form['address'])
      
      if status == 1:
       return render_template("user.html",m1="sucess")
      else:
       return render_template("reg.html",m1="failed")
      

@app.route("/ologin", methods=['GET', 'POST'])       
def ologin():
    if request.method == 'POST':
        status = owner_login(request.form['username'], request.form['password'])
        print(status)
        if status == 1:
            session['username'] = request.form['username']
            return render_template("uhome.html", m1="sucess")
        else:
            return render_template("user.html", m1="Login Failed")

# # -------------------------------Loginact End-----------------------------------------------------------------

# Initialize PorterStemmer and stopwords
ps = PorterStemmer()
stop_words = stopwords.words('english')

# Load the trained models
nb_model = joblib.load('nb_model.pkl')

# Define the TF-IDF vectorizer
tfidf_vect = joblib.load('tfidf_vect.pkl')

# Function to preprocess new text data
def preprocess_new_text(text):
    # Apply the same preprocessing steps as done during training
    text = re.sub('[^a-zA-Z]', ' ', text).lower()
    words = text.split()
    words = [ps.stem(word) for word in words if word not in stop_words]
    processed_text = ' '.join(words)
    return processed_text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        username = request.form['username']
        image = request.form['image']
        new_article = request.form['article']
        
        # Preprocess the new article
        processed_article = preprocess_new_text(new_article)

        # Vectorize the new article using TF-IDF
        tfidf_new_article = tfidf_vect.transform([processed_article])

        # Predictions using the trained models
        nb_prediction = nb_model.predict(tfidf_new_article)[0]

        prediction_label = "True" if nb_prediction == 1 else "Fake"

        print(prediction_label)

        data = predict_act(username,image,new_article,prediction_label)

        return render_template('an.html',  m1="sucess")


   
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
