from app import app
from flask import render_template, flash, redirect, session, request, Flask, url_for
from .forms import LoginForm, ChatForm
import Processer
import sys

proc = Processer.Processor()

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


@app.route('/chat/', methods = ['GET', 'POST'])
def chats():
    form = ChatForm()
    if not 'chatlist' in session:
        session['chatlist'] = []
        flash("Init Chatlist")
    if form.validate_on_submit():
        data = form.inputfield.data
        ans = proc.process_line(str(data))

        new_msg = {'author':{'nickname':'me'},
                   'body': str(data)}
        session['chatlist'].append(new_msg)

        new_ans = {'author':{'nickname':'bot'},
                   'body': ans}
        session['chatlist'].append(new_ans)
        flash(len(session['chatlist']))
    form.inputfield.data = ""
    return render_template('chatUI.html', chats = session['chatlist'], form = form)


def updateview():
    form = ChatForm()
    return render_template('chatUI.html', chats=session['chatlist'], form=form)


