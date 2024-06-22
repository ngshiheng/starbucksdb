from peewee import BooleanField, CharField, Model
from playhouse.sqlite_ext import JSONField, SqliteExtDatabase

db = SqliteExtDatabase("assets/starbucks.db", pragmas={"journal_mode": "wal"})


class BaseModel(Model):
    class Meta:
        database = db


class Store(BaseModel):
    BranchCode = CharField(unique=True)
    OutletCode = CharField()
    StoreCode = CharField()
    StoreName = CharField()
    Address = CharField()
    PostalCode = CharField()
    PhoneNo = CharField()
    Longitude = CharField()
    Latitude = CharField()
    MONPStatus = BooleanField()
    DeliveryStatus = BooleanField()
    OpenNow = BooleanField()
    ServiceHours = JSONField()
    Amenities = JSONField()


def create_tables():
    with db:
        db.create_tables([Store])
