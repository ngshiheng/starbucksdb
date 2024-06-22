from starbucksdb.items import ServiceHourItem, StoreItem


def parse_store_data(store_data):
    service_hours = []
    for service_hour in store_data["ServiceHours"]:
        service_hours.append(
            ServiceHourItem(
                DayOfWeek=service_hour["DayOfWeek"],
                DayOfWeekString=service_hour["DayOfWeekString"],
                OpenFrom=service_hour["OpenFrom"],
                OpenTo=service_hour["OpenTo"],
                Is24Hours=service_hour["Is24Hours"],
                IsClosed=service_hour["IsClosed"],
            )
        )

    return StoreItem(
        BranchCode=store_data["BranchCode"],
        OutletCode=store_data["OutletCode"],
        StoreCode=store_data["StoreCode"],
        StoreName=store_data["StoreName"],
        Address=store_data["Address"],
        PostalCode=store_data["PostalCode"],
        PhoneNo=store_data["PhoneNo"],
        Longitude=store_data["Longitude"],
        Latitude=store_data["Latitude"],
        MONPStatus=store_data["MONPStatus"],
        DeliveryStatus=store_data["DeliveryStatus"],
        OpenNow=store_data["OpenNow"],
        ServiceHours=service_hours,
        Amenities=store_data["Amenities"],
    )
