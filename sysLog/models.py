from django.db import models
from mongoengine import *
from datetime import datetime
# Create your models here.
class syslog(EmbeddedDocument):
    local = StringField(required=True)
    date = StringField(required=True)
    service = StringField(required=True)
    message = StringField(required=True)
