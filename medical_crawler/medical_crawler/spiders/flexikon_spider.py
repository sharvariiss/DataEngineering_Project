import scrapy
from urllib.parse import urljoin

class FlexikonSpider(scrapy.Spider):
    name = "flexikon"
    allowed_domains = ["flexikon.doccheck.com"]
    start_urls = ["https://flexikon.doccheck.com/de/Kategorie:Wirkstoff"]

    def parse(self, response):
        """
        Parse the category page for all active ingredient links.
        """
        article_links = response.css(".mw-category-group a::attr(href)").getall()

        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        # Pagination
        next_page = response.css("a[title='Kategorie:Wirkstoff'] + a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        """
        Extract data from each active ingredient article.
        """
        title = response.css("h1#firstHeading::text").get()
        content = " ".join(response.css(".mw-parser-output p::text").getall())
        image_urls = response.css(".mw-parser-output img::attr(src)").getall()
        image_urls = [urljoin("https://flexikon.doccheck.com", img) for img in image_urls]

        yield {
            "source": "flexikon",
            "url": response.url,
            "title": title,
            "content": content,
            "images": image_urls,
        }
