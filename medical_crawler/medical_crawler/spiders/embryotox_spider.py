import scrapy

class EmbryotoxSpider(scrapy.Spider):
    name = "embryotox"
    allowed_domains = ["embryotox.de"]
    start_urls = ["https://www.embryotox.de/arzneimittel"]

    def parse(self, response):
        """
        Extract all drug links.
        """
        drug_links = response.css("a.Card_link__DpAWu::attr(href)").getall()

        for link in drug_links:
            yield response.follow(link, callback=self.parse_drug)

    def parse_drug(self, response):
        """
        Parse detailed drug information.
        """
        title = response.css("h1::text").get()
        sections = response.css("section")

        content = []
        for sec in sections:
            heading = sec.css("h2::text, h3::text").get()
            text = " ".join(sec.css("p::text").getall())
            if text.strip():
                content.append({"heading": heading, "text": text})

        images = response.css("img::attr(src)").getall()

        yield {
            "source": "embryotox",
            "url": response.url,
            "title": title,
            "content_sections": content,
            "images": images,
        }
