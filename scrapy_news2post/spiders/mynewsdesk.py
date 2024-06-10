from pathlib import Path
import json
import scrapy
import shutil
import re


class MynewsdeskSpider(scrapy.Spider):
    name = "mynewsdesk"
    allowed_domains = ["mynewsdesk.com"]

    def start_requests(self):
        urls = []
        news_urls_path = Path(__file__).resolve().parent.parent.parent.parent / 'urls'
        processed_path = news_urls_path / 'processed'
        processed_path.mkdir(exist_ok=True)

        for file_path in news_urls_path.glob('*.json'):
            with file_path.open('r', encoding='utf-8') as file:
                data = json.load(file)
                urls.append(data['url'])

            shutil.move(str(file_path), str(processed_path / file_path.name))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        main_content = response.xpath('//article[@class="panel"]//text()').getall()
        title = response.xpath('//h1[@class="panel__title"]//text()').get()
        if main_content:
            main_content = ' '.join(main_content).strip()
            main_content = re.sub(r'\s+', ' ', main_content).strip()
            print(main_content)
            yield {'title': title, 'main_content': main_content}
        else:
            self.logger.info('No main content found')
