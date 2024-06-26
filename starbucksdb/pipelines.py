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
            self._process_store_item(adapter)
        elif isinstance(item, MenuItem):
            self._process_menu_item(adapter)

        return item

    def _process_store_item(self, adapter):
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
            "service_hours": [
                dict(service_hours) for service_hours in adapter.get("ServiceHours")
            ],
            "amenities": adapter.get("Amenities"),
        }

        with db.atomic():
            Store.get_or_create(
                branch_code=store_data["branch_code"],
                defaults=store_data,
            )

    def _process_menu_item(self, adapter):
        branch_code = adapter["BranchCode"]
        store = Store.get(Store.branch_code == branch_code)

        for adapter_item in adapter["Items"]:
            with db.atomic():
                menu_item = self._get_or_create_menu_item(store, adapter_item)
                self._update_price_if_changed(store, menu_item, adapter_item)

    def _get_or_create_menu_item(self, store: Store, adapter_item: dict):
        item_data = self._extract_item_data(store, adapter_item)
        menu_item, _ = Item.get_or_create(
            store=store,
            item_id=adapter_item["ItemId"],
            defaults=item_data,
        )
        return menu_item

    def _extract_item_data(self, store: Store, adapter_item: dict):
        return {
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

    def _update_price_if_changed(
        self, store: Store, menu_item: Item, adapter_item: dict
    ):
        new_base_price = adapter_item["BasePrice"]
        new_delivery_price = adapter_item["BasePriceDlvr"]

        last_price = (
            Price.select()
            .where((Price.item == menu_item) & (Price.store == store))
            .order_by(Price.effective_date.desc())
            .first()
        )

        price_has_changed = (
            last_price is None
            or last_price.base_price != new_base_price
            or last_price.delivery_price != new_delivery_price
        )

        if price_has_changed:
            Price.create(
                item=menu_item,
                store=store,
                base_price=new_base_price,
                delivery_price=new_delivery_price,
                effective_date=datetime.date.today(),
            )
