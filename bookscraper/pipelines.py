# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # trail space removal
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()
        # availability
        availability_string_arra = item['availability'].split("(")
        if len(availability_string_arra) < 2:
            item['availability'] = 0
        else:
            availability_string = availability_string_arra[1].split(" ")
            item['availability'] = int(availability_string[0])
        # upper case to lower case
        lowercase_keys = ['category','product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()
        
        # price
        price_keys = ["price_without_tax","tax","price_with_tax","price"]
        for price_key in price_keys:
            value  =  adapter.get(price_key)
            value = value.replace('£','')
            adapter[price_key] = float(value)



        # number_of_rev
        number_reviews_string = adapter.get('number_of_reviews')
        adapter['number_of_reviews'] =  int(number_reviews_string)

        star_text_value = adapter.get('rating')
        
        if star_text_value == "zero":
            adapter['rating'] = 0
        if star_text_value == "one":
            adapter['rating'] == 1
        if star_text_value == "two":
            adapter["rating"] = 2
        if star_text_value == "three":
            adapter['rating'] = 3
        if star_text_value == "four":
            adapter["rating"] = 4
        if star_text_value == "five":
            adapter["rating"] = 5
        

        return item
