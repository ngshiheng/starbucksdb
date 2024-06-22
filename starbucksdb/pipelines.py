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
            Store.insert(**store_data).on_conflict(
                conflict_target=[Store.branch_code], update=store_data
            ).execute()

        return item
