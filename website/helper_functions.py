from random import randint
from .models import Message, Activity
from . import db

def get_image_path(name):
    fileName = ''
    chars = 'xcvbnmQWERTYUI1290qwertyuiopasdfghjklzOPASDFGH345678JKLZXCVBNM'
    for c in name:
        if c not in chars:
            fileName += chars[randint(0, 8)]
        else:
            fileName += c
        fileName += chars[randint(0, 8)]
    return fileName

def set_messages_seen(massegeId):
    msg = Message.query.filter_by(id=massegeId).first()
    if not msg.seen:
        msg.seen = True
    db.session.commit()

def set_activities_seen(actId):
    act = Activity.query.filter_by(id=actId).first()
    if not act.seen:
        act.seen = True
    db.session.commit()