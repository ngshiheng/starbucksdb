import datetime

from itemadapter import ItemAdapter

from starbucksdb.items import MenuItem, StoreItem
from starbucksdb.models.database import Item, Price, Store, create_tables, db


class StarbucksDBPipeline:
    def __init__(self):
        create_tables()

    def open_spider(self, spider):
        db.connect()

    def close_spider(self, spider):
        if not db.is_closed():
            db.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if isinstance(item, StoreItem):
            service_hours = [
                dict(service_hours) for service_hours in adapter.get("ServiceHours")
            ]

            store_data = {
                "branch_code": adapter.get("BranchCode"),
                "outlet_code": adapter.get("OutletCode"),
                "store_code": adapter.get("StoreCode"),
                "store_name": adapter.get("StoreName"),
                "address": adapter.get("Address"),
                "postal_code": adapter.get("PostalCode"),
                "phone_no": adapter.get("PhoneNo"),
                "longitude": adapter.get("Longitude"),
                "latitude": adapter.get("Latitude"),
                "monp_status": adapter.get("MONPStatus"),
                "delivery_status": adapter.get("DeliveryStatus"),
                "open_now": adapter.get("OpenNow"),
                "service_hours": service_hours,
                "amenities": adapter.get("Amenities"),
            }

            with db.atomic():
                store, _ = Store.get_or_create(
                    branch_code=store_data["branch_code"],
                    defaults=store_data,
                )

        elif isinstance(item, MenuItem):
            branch_code = adapter["BranchCode"]
            store = Store.get(Store.branch_code == branch_code)

            for adapter_item in adapter["Items"]:
                item_data = {
                    "store": store,
                    "item_id": adapter_item["ItemId"],
                    "item_code": adapter_item["ItemCode"],
                    "name": adapter_item["Name"],
                    "description": adapter_item["Description"],
                    "photo_urls": adapter_item["PhotoURLs"],
                    "is_mobile_order_pay": adapter_item["IsMOP"],
                    "is_delivery": adapter_item["IsDelivery"],
                    "is_inventoried": adapter_item["IsInventoried"],
                    "is_featured": adapter_item["IsFeatured"],
                    "is_scheduled": adapter_item["IsScheduled"],
                    "is_dine_in": adapter_item["IsDineIn"],
                }

                with db.atomic():
                    menu_item, _ = Item.get_or_create(
                        store=store,
                        item_id=adapter_item["ItemId"],
                        defaults=item_data,
                    )

                    new_base_price = adapter_item["BasePrice"]
                    new_delivery_price = adapter_item["BasePriceDlvr"]

                    last_price = (
                        Price.select()
                        .where((Price.item == menu_item) & (Price.store == store))
                        .order_by(Price.effective_date.desc())
                        .first()
                    )

                    if last_price is None or (
                        last_price.base_price != new_base_price
                        or last_price.delivery_price != new_delivery_price
                    ):
                        # Create a new price entry if there's no previous entry
                        # or if the price has changed
                        Price.create(
                            item=menu_item,
                            store=store,
                            base_price=new_base_price,
                            delivery_price=new_delivery_price,
                            effective_date=datetime.date.today(),
                        )

        return item
