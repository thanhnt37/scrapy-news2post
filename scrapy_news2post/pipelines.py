# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from pathlib import Path


class ScrapyNews2PostPipeline:
    def open_spider(self, spider):
        news_urls_path = Path(__file__).resolve().parent.parent.parent / 'urls/scrapy'
        waiting_path = news_urls_path / 'waiting'
        processed_path = news_urls_path / 'processed'
        processed_path.mkdir(exist_ok=True)
        self.output_path = processed_path

        dynamodb_path = Path(__file__).resolve().parent.parent.parent / 'urls/dynamodb'
        dynamodb_tmp_path = dynamodb_path / 'tmp'
        dynamodb_tmp_path.mkdir(exist_ok=True)
        self.dynamodb_tmp_path = dynamodb_tmp_path

    def process_item(self, item, spider):
        input_file_name = item.get('news_id', None)
        if input_file_name:
            output_file = self.output_path / f"{Path(input_file_name).stem}.json"
            with output_file.open('w', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False, indent=4)

            dynamodb_tmp_output_file = self.dynamodb_tmp_path / f"{Path(input_file_name).stem}.json"
            with dynamodb_tmp_output_file.open('w', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False, indent=4)

        return item

