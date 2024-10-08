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
                    meta = {'news_id': file_path.name, 'url': url}
                    yield scrapy.Request(url=url, callback=self.parse, meta=meta)

            shutil.move(str(file_path), str(processed_path / file_path.name))

    def parse(self, response):
        main_content = response.xpath('//article[@class="panel"]//text()').getall()
        title = response.xpath('//h1[@class="panel__title"]//text()').get()
        published_date = response.xpath('//p[@class="type__date"]/time/@datetime').get()
        first_paragraph = response.xpath('string(//div[@class="panel__text"]/p[1])').get()
        if main_content:
            main_content = ' '.join(main_content).strip()
            main_content = re.sub(r'\s+', ' ', main_content).strip()
            yield {
                'title': title,
                'content': main_content,
                'news_id': response.meta['news_id'],
                'url': response.meta['url'],
                'published_date': published_date,
                'first_paragraph': first_paragraph
            }
        else:
            self.logger.info('No main content found')
