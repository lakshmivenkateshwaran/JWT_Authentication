import scrapy
from itc_data.items import ITCItem


class QuarterlyResultsSpider(scrapy.Spider):
    name = 'quarterly_results'
    start_urls = [
        'https://www.itcportal.com/media-centre/press-releases-content.aspx?id=2743&type=C&news=media-statement-financial-results-for-the-quarter-ended-30th-september-2024'
    ]

    def parse(self, response):
        # Find links to PDF files
        for link in response.css('a::attr(href)').getall():
            if link.endswith('.pdf'):  # Only process PDF links
                file_url = response.urljoin(link)  # Join relative URL with the base URL
                self.logger.info(f"Found PDF: {file_url}")
                yield ITCItem(file_urls=[file_url])
