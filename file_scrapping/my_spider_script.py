import scrapy
import logging

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['http://127.0.0.1:8080/.hidden/']

    def parse(self, response):
        # Extract the links
        links = response.css('pre a::attr(href)').extract()

        for link in links:
            if link.endswith('/'):
                # If it's a directory, recursively follow the link
                yield scrapy.Request(response.urljoin(link), callback=self.parse)
            else:
                # If it's a file, check if it's a README file
                if 'README' in link:
                    yield scrapy.Request(response.urljoin(link), callback=self.parse_file)

    def parse_file(self, response):
        # Extract the content of the file
        file_content = response.body.decode('utf-8')
        # Log the URL and content
        readme_url = response.url

        if "flag" in file_content:
            logging.info(f'{readme_url} : {file_content}')

# Set the logging level to INFO
logging.getLogger('scrapy').setLevel(logging.INFO)
