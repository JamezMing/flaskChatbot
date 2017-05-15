from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm, ChatForm

chats = []

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login Requested for Openid = '%s', remember_me = %s " % (form.openid.data, str(form.remember_me.data)))
        return redirect(('/index'))
    return render_template('login.html', title = "Sign In", form = form)

@app.route('/chat', methods = ['GET', 'POST'])
def chat():
    form = ChatForm()
    return render_template('chatUI.html', chats = chats, form = form)


