from scrapy import Item, Field

class HotelItem(Item):
    propertyTitle = Field()
    rating = Field()
    location = Field()
    latitude = Field()
    longitude = Field()
    room_type = Field()
    price = Field()
    img = Field()
    image_urls = Field()
    images = Field()