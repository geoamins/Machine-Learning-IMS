import json
from itemadapter import ItemAdapter

class ScrapyExamplePipeline:
    def __init__(self):
        self.file = open('books.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True

    def process_item(self, item, spider):
        line = json.dumps(
            dict(item),
            ensure_ascii=False,
            indent=2
        )
        
        if not self.first_item:
            self.file.write(',\n')
        self.first_item = False
        
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close() 