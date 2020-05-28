from django.db import models
#from sysLog.models import syslog
from mongoengine import *
from datetime import datetime
# Create your models here.

class syslog(EmbeddedDocument):
    local = StringField(required=True)
    date = DateTimeField(required=True)
    service = StringField(required=True)
    message = StringField(required=True)


    
class Server(EmbeddedDocument):
    host = StringField(required=True)
    port = IntField(required=True)
    user = StringField(required=True)
    password = StringField(required=True)
    syslogs = EmbeddedDocumentListField(document_type=syslog)


class User (Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    password = StringField(required=True)
    servers = EmbeddedDocumentListField(document_type=Server)




