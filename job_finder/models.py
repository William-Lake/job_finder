from peewee import *

database = PostgresqlDatabase('job_finder', **{'host': '127.0.0.1', 'user': 'jobs_admin', 'password': 'jobs_admin'})

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
        schema = 'jobs'

class Job(BaseModel):
    contest_num = IntegerField()
    date_closed = DateField(null=True)
    date_opened = DateField()
    dept = TextField()
    site_id = IntegerField()
    site_url = TextField()
    title = TextField()

    class Meta:
        table_name = 'job'
        schema = 'jobs'

class Prop(BaseModel):
    email = CharField()
    is_selected = BooleanField(constraints=[SQL("DEFAULT false")])
    port = IntegerField()
    pword = CharField()
    smtp = CharField()

    class Meta:
        table_name = 'prop'
        schema = 'jobs'

class Recipient(BaseModel):
    date_added = DateField()
    email = TextField()

    class Meta:
        table_name = 'recipient'
        schema = 'jobs'

