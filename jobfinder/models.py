from peewee import *

database = SqliteDatabase(None)

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Appdata(BaseModel):
    author = TextField(null=True)
    copyright = TextField(null=True)
    email = TextField(null=True)
    license = TextField(null=True)
    status = TextField(null=True)
    version = TextField(null=True)

    class Meta:
        table_name = 'appdata'
        primary_key = False

class Job(BaseModel):
    contest_num = IntegerField(null=True)
    date_closed = IntegerField(null=True)
    date_opened = IntegerField(null=True)
    dept = TextField(null=True)
    id = IntegerField(null=True)
    site_id = IntegerField(null=True)
    site_url = TextField(null=True)
    title = TextField(null=True)

    class Meta:
        table_name = 'job'
        primary_key = False

class Props(BaseModel):
    email = CharField()
    port = IntegerField()
    pword = CharField()
    smtp = CharField()

    class Meta:
        table_name = 'props'

class Recipient(BaseModel):
    date_added = IntegerField(null=True)
    email = TextField(null=True)

    class Meta:
        table_name = 'recipient'

