# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from pathlib import Path


class ScrapyNews2PostPipeline:
    def open_spider(self, spider):
        self.output_path = Path(__file__).resolve().parent.parent.parent / 'urls'
        langchain_path = self.output_path / 'langchain'
        langchain_path.mkdir(exist_ok=True)
        langchain_waiting_path = langchain_path / 'waiting'
        langchain_waiting_path.mkdir(exist_ok=True)
        self.output_path = langchain_waiting_path

    def process_item(self, item, spider):
        input_file_name = item.pop('input_file_name', None)
        if input_file_name:
            output_file = self.output_path / f"{Path(input_file_name).stem}.json"

            with output_file.open('w', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False, indent=4)

        return item

