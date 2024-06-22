import scrapy


class StoreItem(scrapy.Item):
    BranchCode = scrapy.Field()
    OutletCode = scrapy.Field()
    StoreCode = scrapy.Field()
    StoreName = scrapy.Field()
    Address = scrapy.Field()
    PostalCode = scrapy.Field()
    PhoneNo = scrapy.Field()
    Longitude = scrapy.Field()
    Latitude = scrapy.Field()
    MONPStatus = scrapy.Field()
    DeliveryStatus = scrapy.Field()
    OpenNow = scrapy.Field()  # TODO: delete. not required
    ServiceHours = scrapy.Field()
    Amenities = scrapy.Field()


class ServiceHourItem(scrapy.Item):
    DayOfWeek = scrapy.Field()
    DayOfWeekString = scrapy.Field()
    OpenFrom = scrapy.Field()
    OpenTo = scrapy.Field()
    Is24Hours = scrapy.Field()
    IsClosed = scrapy.Field()
    # BranchCode = scrapy.Field()


class AmenityItem(scrapy.Item):
    Is24Hours = scrapy.Field()  # "24Hours"
    Cashless = scrapy.Field()
    FreeWifi = scrapy.Field()
    MobileOrderandPay = scrapy.Field()
    NitroColdBrew = scrapy.Field()
    StarbucksReserve = scrapy.Field()
    # StoreCode = scrapy.Field()
