from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = 'generate_a_secrete_key'
db = SQLAlchemy(app)


class MapleUser(db.Model):
    __tablename__ = 'maple_user'

    phone = db.Column(db.String(255), primary_key=True)
    nickname = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    auth = db.Column(db.Enum('0', '1'))

    def __init__(self, phone, nickname, password, auth):
        self.phone = phone
        self.nickname = nickname
        self.password = password
        self.auth = auth


class Seat(db.Model):
    __tablename__ = 'seat'

    s_num = db.Column(db.Integer, primary_key=True, nullable=False)
    c_num = db.Column(db.Integer, primary_key=True, nullable=False)
    train_num = db.Column(db.String(10), primary_key=True, nullable=False)


class Ticket(db.Model):
    __tablename__ = 'ticket'

    date = db.Column(db.Date, primary_key=True, nullable=False)
    train_num = db.Column(db.String(10), primary_key=True, nullable=False)
    c_num = db.Column(db.Integer, primary_key=True, nullable=False)
    s_num = db.Column(db.Integer, primary_key=True, nullable=False)
    start = db.Column(db.String(10), primary_key=True, nullable=False)
    destination = db.Column(db.String(10), primary_key=True, nullable=False)
    p_num = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    u_num = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)


class TimeTable(db.Model):
    __tablename__ = 'time_table'

    train_num = db.Column(db.String(10), primary_key=True)
    arrive_time = db.Column(db.String(5), nullable=False)
    leave_time = db.Column(db.String(5), nullable=False)
    place = db.Column(db.String(10), primary_key=True)


class Train(db.Model):
    __tablename__ = 'train'

    train_num = db.Column(db.String(10), primary_key=True)
    start_time = db.Column(db.String(5))
    end_time = db.Column(db.String(5))
    start = db.Column(db.String(10))
    destination = db.Column(db.String(10))

