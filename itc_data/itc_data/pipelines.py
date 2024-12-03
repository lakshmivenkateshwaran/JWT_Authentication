# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
import os

class CustomFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        """
        Customize the path where the downloaded file will be saved.
        """
        # Extract the filename from the URL
        parsed_url = urlparse(request.url)
        filename = os.path.basename(parsed_url.path)
        return f"files/{filename}"


