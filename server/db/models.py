from peewee import Model, CharField, TextField, BooleanField, ForeignKeyField, UUIDField, MySQLDatabase, SqliteDatabase
import os
from uuid import uuid4

db = MySQLDatabase(
    os.getenv("MYSQLDATABASE", "railway"),
    user=os.getenv("MYSQLUSER", "root"),
    password=os.getenv("MYSQLPASSWORD", "hVOFYvCKTUaVNvbbzkzVaNoaiWnANUPm"),
    host=os.getenv("MYSQLHOST", "localhost"),
    port=int(os.getenv("MYSQLPORT", 3306))  # Default MySQL port
)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)

class Action(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(unique=True)
    description = TextField()

class Macro(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKeyField(User, backref='macros', on_delete='CASCADE')
    name = CharField()
    prompt = TextField()
    allow_other_actions = BooleanField(default=False)

class MacroAction(BaseModel):
    macro = ForeignKeyField(Macro, backref='required_actions', on_delete='CASCADE')
    action = ForeignKeyField(Action, backref='in_macros', on_delete='CASCADE')

class UserAction(BaseModel):
    user = ForeignKeyField(User, backref='actions', on_delete='CASCADE')
    action = ForeignKeyField(Action, backref='used_by', on_delete='CASCADE')