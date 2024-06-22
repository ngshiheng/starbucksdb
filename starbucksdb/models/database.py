import datetime

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
)
from playhouse.sqlite_ext import JSONField, SqliteExtDatabase

db = SqliteExtDatabase("assets/starbucks.db", pragmas={"journal_mode": "wal"})


class BaseModel(Model):
    class Meta:
        database = db


class Store(BaseModel):
    branch_code = CharField(unique=True)
    outlet_code = CharField()
    store_code = CharField()
    store_name = CharField()
    address = CharField()
    postal_code = CharField()
    phone_no = CharField()
    longitude = FloatField()
    latitude = FloatField()
    monp_status = BooleanField()
    delivery_status = BooleanField()
    open_now = BooleanField()
    service_hours = JSONField()
    amenities = JSONField()

    class Meta:
        table_name = "stores"
        indexes = (
            (
                ("longitude", "latitude"),
                False,
            ),
        )


class Item(BaseModel):
    store = ForeignKeyField(Store, backref="items")
    item_id = CharField()
    item_code = CharField(null=True)
    name = CharField()
    description = CharField()
    photo_urls = JSONField()
    # sequence = FloatField()
    # pmt_no = CharField(null=True)
    # pmt_ref_no = CharField(null=True)
    # pmt_amount = IntegerField(null=True)
    # pmt_line = IntegerField(null=True)
    is_mobile_order_pay = BooleanField()
    is_delivery = BooleanField()
    is_inventoried = BooleanField()
    is_featured = BooleanField()
    is_scheduled = BooleanField()
    is_dine_in = BooleanField()

    class Meta:
        table_name = "menu_items"
        indexes = (
            (("store", "item_id"), True),
            (("store", "name"), False),
        )


class Price(BaseModel):
    item = ForeignKeyField(Item, backref="prices")
    store = ForeignKeyField(Store, backref="prices")
    base_price = IntegerField()
    delivery_price = IntegerField()
    effective_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "item_prices"
        indexes = ((("item", "store"), True),)


def create_tables():
    with db:
        db.create_tables([Store, Item, Price])
