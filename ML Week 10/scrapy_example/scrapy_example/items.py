import scrapy

class BookItem(scrapy.Item):
    # Define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field() 