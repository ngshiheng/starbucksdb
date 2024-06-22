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
    OpenNow = scrapy.Field()
    ServiceHours = scrapy.Field()
    Amenities = scrapy.Field()


class ServiceHourItem(scrapy.Item):
    DayOfWeek = scrapy.Field()
    DayOfWeekString = scrapy.Field()
    OpenFrom = scrapy.Field()
    OpenTo = scrapy.Field()
    Is24Hours = scrapy.Field()
    IsClosed = scrapy.Field()


class AmenityItem(scrapy.Item):
    Is24Hours = scrapy.Field()  # "24Hours"
    Cashless = scrapy.Field()
    FreeWifi = scrapy.Field()
    MobileOrderandPay = scrapy.Field()
    NitroColdBrew = scrapy.Field()
    StarbucksReserve = scrapy.Field()


class MenuItem(scrapy.Item):
    LastUpdated = scrapy.Field()
    BranchCode = scrapy.Field()
    ServiceHours = scrapy.Field()
    Categories = scrapy.Field()
    Items = scrapy.Field()


class ItemItem(scrapy.Item):
    ItemId = scrapy.Field()
    ItemCode = scrapy.Field()
    Name = scrapy.Field()
    Description = scrapy.Field()
    BasePrice = scrapy.Field()
    BasePriceDlvr = scrapy.Field()
    PhotoURLs = scrapy.Field()
    Sequence = scrapy.Field()
    ModifierGroup = scrapy.Field()
    PMTNo = scrapy.Field()
    PMTRefNo = scrapy.Field()
    PMTAmount = scrapy.Field()
    PMTLine = scrapy.Field()
    IsMOP = scrapy.Field()
    IsDelivery = scrapy.Field()
    IsInventoried = scrapy.Field()
    IsFeatured = scrapy.Field()
    IsScheduled = scrapy.Field()
    IsDineIn = scrapy.Field()
