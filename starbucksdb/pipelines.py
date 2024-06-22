from itemadapter import ItemAdapter

from starbucksdb.items import MenuItem, StoreItem
from starbucksdb.models.database import Item, Store, create_tables, db


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

            for menu_item in adapter["Items"]:
                item_data = {
                    "store": store,
                    "item_id": menu_item["ItemId"],
                    "item_code": menu_item["ItemCode"],
                    "name": menu_item["Name"],
                    "description": menu_item["Description"],
                    "photo_urls": menu_item["PhotoURLs"],
                    "is_mobile_order_pay": menu_item["IsMOP"],
                    "is_delivery": menu_item["IsDelivery"],
                    "is_inventoried": menu_item["IsInventoried"],
                    "is_featured": menu_item["IsFeatured"],
                    "is_scheduled": menu_item["IsScheduled"],
                    "is_dine_in": menu_item["IsDineIn"],
                }

                with db.atomic():
                    i, _ = Item.get_or_create(
                        store=store,
                        item_id=menu_item["ItemId"],
                        defaults=item_data,
                    )

                    price_data = {
                        "item": i,
                        "store": store,
                        "base_price": adapter.get("BasePrice", 0),
                        "delivery_price": adapter.get("BasePriceDlvr", 0),
                    }

                    # price = Price(
                    #     item=item,
                    #     store=store,
                    #     base_price=int(price_data["base_price"]),
                    #     delivery_price=int(price_data["delivery_price"]),
                    #     effective_date=datetime.datetime.now(),
                    # )
                    # price.save()

        return item
