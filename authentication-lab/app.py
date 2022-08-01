from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {

  "apiKey": "AIzaSyBv3RtFdQFHXvRX5t9weTwRdC93KbKVLqE",

  "authDomain": "cs-groupf.firebaseapp.com",

  "projectId": "cs-groupf",

  "storageBucket": "cs-groupf.appspot.com",

  "messagingSenderId": "944795672547",

  "appId": "1:944795672547:web:26cd6c1f6ec868cef30ad6",

  "measurementId": "G-EL98484YH3" , "databaseURL":"https://cs-groupf-default-rtdb.europe-west1.firebasedatabase.app/"

}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))  
        except:
            error = "Authentication failed"

            return render_template("signin.html")

    else:
        return render_template("signin.html")


        




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        username = request.form['username']
        bio = request.form['bio']
        user={"email": email , "password": password , "username": username , "fullname": fullname}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))

        except:
            error = "Authentication failed"
        return render_template("signup.html")

    else:
        return render_template("signup.html")




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        try:
            title = request.form['title']
            text = request.form['text']
            tweet={"title": title , "text": text , "uid": login_session['user']['localId']}
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error="Tweet failed"
            return render_template("add_tweet.html")
    else:
        return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():

    tweets=db.child("Tweets").get().val()
    return render_template("all_tweets.html",tweets=tweets)



if __name__ == '__main__':
    app.run(debug=True)