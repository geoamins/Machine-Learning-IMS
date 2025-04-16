import scrapy
from scrapy_example.items import BookItem

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # Extract book links
        book_links = response.css('article.product_pod h3 a::attr(href)').getall()
        
        # Follow each book link
        for book_link in book_links:
            yield response.follow(book_link, callback=self.parse_book)
        
        # Follow next page link if exists
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        item = BookItem()
        
        # Extract book information
        item['title'] = response.css('h1::text').get()
        item['price'] = response.css('p.price_color::text').get()
        item['availability'] = response.css('p.availability::text').getall()[1].strip()
        item['rating'] = response.css('p.star-rating::attr(class)').get().split()[-1]
        item['description'] = response.css('div#product_description + p::text').get()
        item['url'] = response.url
        
        yield item 