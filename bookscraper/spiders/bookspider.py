import scrapy
# import item
from bookscraper.items import BookItem
import random
class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    ]

    def parse(self, response):
        # Extracting the content using css selectors
        books = response.css("article.product_pod")
        for book in books:
            relative_url = book.css("h3 a").attrib["href"]
            
            yield response.follow(relative_url, self.parse_book,headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list) - 1)]})
        next_page = response.css(".next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse,headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list) - 1)]})
    def parse_book(self, response):
        bookItem = BookItem()
        table_rows = response.css("table tr")

    
        bookItem["title"] = response.css("h1::text").get(),
        bookItem["url"] = response.url,
        bookItem[ "price"] =  response.css(".price_color::text").get(),
        bookItem[ "upc"] =  table_rows[0].css("td::text").get(),
        bookItem[ "product_type"]= table_rows[1].css("td::text").get(),
        bookItem["price_without_tax"]= table_rows[2].css("td::text").get(),
        bookItem[ "price_with_tax"]= table_rows[3].css("td::text").get(),
        bookItem[ "tax"]= table_rows[4].css("td::text").get(),
        bookItem[ "availability"]=  table_rows[5].css("td::text").get(),
        bookItem["number_of_reviews"]=  table_rows[6].css("td::text").get(),
        bookItem["description"]=  response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        bookItem[ "rating"] = response.css("p.star-rating").attrib["class"].split()[-1],
        bookItem[ "category"] = response.css(".breadcrumb a::text").getall()[2],
        yield bookItem