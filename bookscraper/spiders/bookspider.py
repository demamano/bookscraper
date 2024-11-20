import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        # Extracting the content using css selectors
        books = response.css("article.product_pod")
        for book in books:
            relative_url = book.css("h3 a").attrib["href"]
            
            yield response.follow(relative_url, self.parse_book)
        next_page = response.css(".next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
    def parse_book(self, response):
        table_rows = response.css("table tr")

        yield {
    "title" :response.css("h1::text").get(),
    "price": response.css(".price_color::text").get(),
    "upc": table_rows[0].css("td::text").get(),
    "product_type": table_rows[1].css("td::text").get(),
    "price_without_tax": table_rows[2].css("td::text").get(),
    "price_with_tax": table_rows[3].css("td::text").get(),
    "tax": table_rows[4].css("td::text").get(),
    "availability": table_rows[5].css("td::text").get(),
    "number_of_reviews": table_rows[6].css("td::text").get(),
    "description": response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
    "rating": response.css("p.star-rating").attrib["class"].split()[-1],
    "category": response.css(".breadcrumb a::text").getall()[2],
       }