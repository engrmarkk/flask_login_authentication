
from flask import Flask, render_template, url_for, redirect, request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, LoginManager, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, template_folder="template")

base_dir = os.path.dirname(os.path.realpath(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_dir, "user.db")
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='ec129bf735e62f2a277a9e1c'

db = SQLAlchemy(app)

login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    confirm = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'user <{self.username}>'

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login_post():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("index"))
    else:
        return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup_post():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password =  request.form.get("password")
        confirm = request.form.get("confirm")

        user = User.query.filter_by(username=username).first()
        if user :
            flash("Username already exists")
            return redirect(url_for('signup_post'))
        

        user_email =  User.query.filter_by(email=email).first()
        if user_email :
            flash("Email address already exists")
            return redirect(url_for('signup_post'))


        password_hash = generate_password_hash(password)
        confirm = generate_password_hash(confirm)

        new_user = User(username=username,  email=email, password_hash=password_hash, confirm=confirm)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login_post"))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    logout_user()
    return render_template("index.html")

@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)