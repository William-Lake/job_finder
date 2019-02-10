from peewee import *

database = PostgresqlDatabase('jobs', **{'host': '127.0.0.1', 'user': 'jobs_admin', 'password': 'jobs_admin'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class DatabaseInfo(BaseModel):
    author = CharField(null=True)
    db_version = CharField(null=True)
    last_update = DateField(null=True)

    class Meta:
        table_name = 'database_info'

class Job(BaseModel):
    contest_num = BigIntegerField()
    date_closed = DateField(null=True)
    date_opened = DateField()
    dept = TextField()
    site_id = BigIntegerField()
    site_url = TextField()
    title = TextField()

    class Meta:
        table_name = 'job'

class Prop(BaseModel):
    is_selected = BooleanField(constraints=[SQL("DEFAULT false")])
    smtp = CharField()
    port = IntegerField()
    email = CharField()
    pword = CharField()

    class Meta:
        table_name = 'prop'

class Recipient(BaseModel):
    data_added = DateField()
    email = TextField()

    class Meta:
        table_name = 'recipient'

