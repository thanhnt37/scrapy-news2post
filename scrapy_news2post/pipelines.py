# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from pathlib import Path


class ScrapyNews2PostPipeline:
    def open_spider(self, spider):
        self.output_path = Path(__file__).resolve().parent.parent.parent / 'urls/output'
        self.output_path.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        input_file_name = item.pop('input_file_name', None)
        if input_file_name:
            output_file = self.output_path / f"{Path(input_file_name).stem}_output.json"

            with output_file.open('w', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False, indent=4)

        return item

