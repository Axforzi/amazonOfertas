# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import datetime
from styleframe import StyleFrame

class ToDictPipeline:
    def process_item(self, item, spider):
        item['discount'] = '-' + item['discount']
        return dict(item)

class ToDataFramePipeline:
    def open_spider(self, spider):
        self.products = []

    def process_item(self, item, spider):
        self.products.append(item)
        return item
    
    def close_spider(self, spider):
        data = pd.DataFrame(self.products)
        now = datetime.datetime.now()
        name = now.strftime("%d-%m-%Y_%H-%M-%S") + '-products_offerts.xlsx'

        writer = pd.ExcelWriter(name, engine='xlsxwriter')
        data.to_excel(writer, index=False, sheet_name='Sheet1')

        # get the XlsxWriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # adjust the column widths based on the content
        for i, col in enumerate(data.columns):
            width = max(data[col].apply(lambda x: len(str(x))).max(), len(col))
            worksheet.set_column(i, i, width)

        worksheet.set_column(0, 0, 50)
        writer.close()