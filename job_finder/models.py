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
    content_num = IntegerField()
    date_closed = DateField(null=True)
    date_opened = DateField()
    dept = TextField()
    site_id = IntegerField()
    site_url = TextField()
    title = TextField()

    class Meta:
        table_name = 'job'
        schema = 'jobs'

class OpenJobView(BaseModel):
    content_num = IntegerField(null=True)
    date_closed = DateField(null=True)
    date_opened = DateField(null=True)
    dept = TextField(null=True)
    id = IntegerField(null=True)
    site_id = IntegerField(null=True)
    site_url = TextField(null=True)
    title = TextField(null=True)

    class Meta:
        table_name = 'open_job_view'
        schema = 'jobs'
        primary_key = False

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
    data_added = DateField()
    email = TextField()

    class Meta:
        table_name = 'recipient'
        schema = 'jobs'

