from playhouse.db_url import connect
from peewee import Model, CharField, TextField, BooleanField, ForeignKeyField, UUIDField
import os
from uuid import uuid4

db = connect(os.getenv("DATABASE_URL", "sqlite:///hem.db"))

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