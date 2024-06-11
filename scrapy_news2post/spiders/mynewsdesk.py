from pathlib import Path
import json
import scrapy
import shutil
import re


class MynewsdeskSpider(scrapy.Spider):
    name = "mynewsdesk"
    allowed_domains = ["mynewsdesk.com"]

    def start_requests(self):
        news_urls_path = Path(__file__).resolve().parent.parent.parent.parent / 'urls/scrapy'
        waiting_path = news_urls_path / 'waiting'
        processed_path = news_urls_path / 'processed'
        processed_path.mkdir(exist_ok=True)

        for file_path in waiting_path.glob('*.json'):
            with file_path.open('r', encoding='utf-8') as file:
                data = json.load(file)
                url = data.get('url')
                if url:
                    meta = {'input_file_name': file_path.name}
                    yield scrapy.Request(url=url, callback=self.parse, meta=meta)

            shutil.move(str(file_path), str(processed_path / file_path.name))

    def parse(self, response):
        main_content = response.xpath('//article[@class="panel"]//text()').getall()
        title = response.xpath('//h1[@class="panel__title"]//text()').get()
        if main_content:
            main_content = ' '.join(main_content).strip()
            main_content = re.sub(r'\s+', ' ', main_content).strip()
            yield {
                'title': title,
                'main_content': main_content,
                'input_file_name': response.meta['input_file_name']
            }
        else:
            self.logger.info('No main content found')
