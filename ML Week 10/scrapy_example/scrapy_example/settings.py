BOT_NAME = 'scrapy_example'

SPIDER_MODULES = ['scrapy_example.spiders']
NEWSPIDER_MODULE = 'scrapy_example.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 2

# Disable cookies
COOKIES_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
   'scrapy_example.pipelines.ScrapyExamplePipeline': 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncio.ReactorAsyncio'
FEED_EXPORT_ENCODING = 'utf-8' 