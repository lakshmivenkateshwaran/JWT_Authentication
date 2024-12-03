# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ITCItem(scrapy.Item):
    file_urls = scrapy.Field()  # URLs to be downloaded
    files = scrapy.Field()  # Metadata of downloaded files
