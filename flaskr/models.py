import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr import login_manager
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    notices = db.relationship('Notice', backref='author', lazy='dynamic')

    events = db.relationship('Event', backref='author', lazy='dynamic')

    event_details = db.relationship('EventDetail', backref='user',
                                    lazy='dynamic')
    resources = db.relationship('Resource', backref='author', lazy='dynamic')

    # 只写密码及其验证函数
    @property
    def password(self):
        raise AttributeError('password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Notice(db.Model):
    __tablename__ = 'notices'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author_id = db.Column(db.ForeignKey('users.id'))


class EventClass(db.Model):
    __tablename__ = 'eventclass'

    id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(20))
    events = db.relationship('Event', backref='eventclass', lazy='dynamic')

    @staticmethod
    def insert_event_classes():
        event_classes = ['机房建设', '客户施工', '机房维护']
        for i in event_classes:
            event_class = EventClass.query.filter_by(classname=i).first()
            if event_class is None:
                event_class = EventClass(classname=i)
            db.session.add(event_class)
        db.session.commit()


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_time = db.Column(db.DateTime)
    end = db.Column(db.Boolean, index=True, default=False)
    author_id = db.Column(db.ForeignKey('users.id'))
    class_id = db.Column(db.ForeignKey('eventclass.id'))
    event_details = db.relationship('EventDetail', backref='event', lazy='dynamic')


class EventDetail(db.Model):
    __tablename__ = 'event_details'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(128))
    link = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    resource_class = db.Column(db.Integer, db.ForeignKey('resourceclasses.id'), default=2)


class ResourceClass(db.Model):
    __tablename__ = 'resourceclasses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    resources = db.relationship('Resource', backref='klass', lazy='dynamic')

    @staticmethod
    def insert_resource_class():
        resources = ['profession', 'tool', 'other']
        for i in resources:
            klass = ResourceClass.query.filter_by(name=i).first()
            if klass == None:
                resourceClass = ResourceClass(name=i)
                db.session.add(resourceClass)
        db.session.commit()
