from itemadapter import ItemAdapter

from starbucksdb.models.database import Store, create_tables, db


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

        service_hours = [
            dict(service_hours) for service_hours in adapter.get("ServiceHours")
        ]

        store_data = {
            "BranchCode": adapter.get("BranchCode"),
            "OutletCode": adapter.get("OutletCode"),
            "StoreCode": adapter.get("StoreCode"),
            "StoreName": adapter.get("StoreName"),
            "Address": adapter.get("Address"),
            "PostalCode": adapter.get("PostalCode"),
            "PhoneNo": adapter.get("PhoneNo"),
            "Longitude": adapter.get("Longitude"),
            "Latitude": adapter.get("Latitude"),
            "MONPStatus": adapter.get("MONPStatus"),
            "DeliveryStatus": adapter.get("DeliveryStatus"),
            "OpenNow": adapter.get("OpenNow"),
            "ServiceHours": service_hours,
            "Amenities": adapter.get("Amenities"),
        }

        with db.atomic():
            Store.insert(**store_data).on_conflict(
                conflict_target=[Store.BranchCode], update=store_data
            ).execute()

        return item
