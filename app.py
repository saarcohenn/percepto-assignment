from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, current_user, login_required
from flask_security.forms import RegisterForm
from wtforms import StringField, TextAreaField
from flask_wtf import FlaskForm
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///forum.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'somesaltfortheforum'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Creating Roles
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# DB Tables
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(250))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    # BackRefs
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    threads = db.relationship('Thread', backref='user', lazy='dynamic')
    replies = db.relationship('Reply', backref='user', lazy='dynamic')

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(35))
    description = db.Column(db.String(300))
    date_created = db.Column(db.DateTime())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    
    # BackRefs
    replies = db.relationship('Reply', backref='thread', lazy='dynamic')

    def last_action_date(self):
        last_reply = Reply.query.filter_by(thread_id=self.id).order_by(Reply.id.desc()).first()
        if last_reply:
            return last_reply.date_created
        return self.date_created

    def get_replies(self):
        return Reply.query.filter_by(thread_id=self.id).all()


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(300))
    date_created = db.Column(db.DateTime())


# Forms
class ExtendRegisterForm(RegisterForm):
    name = StringField("Name")
    username = StringField("Username")

class NewThread(FlaskForm):
    title = StringField("Title")
    description = StringField("Description")

class NewReply(FlaskForm):
    message = TextAreaField('Message')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendRegisterForm)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NewThread()
    if form.validate_on_submit():
        new_thread = Thread(title=form.title.data, description=form.description.data, 
        date_created=datetime.now(), created_by=current_user.id)
        db.session.add(new_thread)
        db.session.commit()
        return redirect(url_for('index'))
    
    threads = Thread.query.all()

    return render_template('index.html', form=form, threads=threads, current_user=current_user)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)

@app.route('/thread/<thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    form = NewReply()
    thread = Thread.query.get(int(thread_id))

    if form.validate_on_submit():
        reply = Reply(user_id = current_user.id, message=form.message.data, date_created=datetime.now())
        thread.replies.append(reply)
        db.session.commit()
        return redirect(url_for('thread', thread_id=thread_id))
        
    
    replies = Reply.query.filter_by(thread_id=thread_id).all()
    return render_template('thread.html', thread=thread, form=form, replies=replies, current_user=current_user)


@app.route('/delete/reply/<int:thread_id>&<int:reply_id>')
def delete_reply(thread_id, reply_id):
    reply_to_delete = Reply.query.get_or_404(reply_id)
    try:
        db.session.delete(reply_to_delete)
        db.session.commit()
        return redirect(url_for('thread', thread_id=thread_id))
    except:
        return "There was a problem deleting the reply"

@app.route('/delete/thread/<int:id>')
def delete_thread(id):
    thread_to_delete = Thread.query.get_or_404(id)
    try:
        for reply in thread_to_delete.replies:
            db.session.delete(reply)
        db.session.delete(thread_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was a problem deleting the thread"
