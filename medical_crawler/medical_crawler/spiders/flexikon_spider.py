# import scrapy
# from urllib.parse import urljoin

# class FlexikonSpider(scrapy.Spider):
#     name = "flexikon"
#     allowed_domains = ["flexikon.doccheck.com"]
#     start_urls = ["https://flexikon.doccheck.com/de/Kategorie:Wirkstoff"]

#     def parse(self, response):
#         """
#         Parse the category page for all active ingredient links.
#         """
#         article_links = response.css(".mw-category-group a::attr(href)").getall()

#         for link in article_links:
#             yield response.follow(link, callback=self.parse_article)

#         # Pagination
#         next_page = response.css("a[title='Kategorie:Wirkstoff'] + a::attr(href)").get()
#         if next_page:
#             yield response.follow(next_page, callback=self.parse)

#     def parse_article(self, response):
#         """
#         Extract data from each active ingredient article.
#         """
#         title = response.css("h1#firstHeading::text").get()
#         content = " ".join(response.css(".mw-parser-output p::text").getall())
#         image_urls = response.css(".mw-parser-output img::attr(src)").getall()
#         image_urls = [urljoin("https://flexikon.doccheck.com", img) for img in image_urls]

#         yield {
#             "source": "flexikon",
#             "url": response.url,
#             "title": title,
#             "content": content,
#             "images": image_urls,
#         }

# 


import scrapy
from urllib.parse import urljoin

class FlexikonAsaSpider(scrapy.Spider):
    name = "flexikon_asa_detail"
    allowed_domains = ["flexikon.doccheck.com"]
    start_urls = [
        "https://flexikon.doccheck.com/de/Acetylsalicyls%C3%A4ure"
    ]

    def get_section(self, response, section_id):
        """
        Extract all text belonging to a MediaWiki section by span id.
        """
        xpath = f"""
        //span[@id='{section_id}']
        /parent::h2
        /following-sibling::*[
            not(self::h2)
        ]
        """
        nodes = response.xpath(xpath)
        texts = []
        for node in nodes:
            if node.root.tag == "h2":
                break
            text = " ".join(node.xpath(".//text()").getall())
            text = " ".join(text.split())
            if text:
                texts.append(text)
        return "\n\n".join(texts) if texts else None

    def get_subsection(self, response, section_id):
        xpath = f"""
        //span[@id='{section_id}']
        /parent::h3
        /following-sibling::*[
            not(self::h3)
        ]
        """
        nodes = response.xpath(xpath)
        texts = []
        for node in nodes:
            if node.root.tag == "h3":
                break
            text = " ".join(node.xpath(".//text()").getall())
            text = " ".join(text.split())
            if text:
                texts.append(text)
        return "\n\n".join(texts) if texts else None

    def parse(self, response):
        base = "https://flexikon.doccheck.com"

        yield {
            "source": "flexikon",
            "url": response.url,
            "title": response.css("h1#firstHeading::text").get(),

            "definition": self.get_section(response, "Definition"),
            "history": self.get_section(response, "Geschichte"),
            "chemistry": self.get_section(response, "Chemie"),
            "mechanism_of_action": self.get_section(response, "Wirkmechanismus"),

            "mechanism_cox1": self.get_subsection(response, "Wirkung_auf_COX-1"),
            "mechanism_cox2": self.get_subsection(response, "Wirkung_auf_COX-2"),

            "pharmacokinetics": self.get_section(response, "Pharmakokinetik"),
            "indications": self.get_section(response, "Indikationen"),
            "dosage": self.get_section(response, "Dosierung"),
            "prescription_requirement": self.get_section(response, "Verschreibungspflicht"),
            "side_effects": self.get_section(response, "Nebenwirkungen"),
            "interactions": self.get_section(response, "Wechselwirkungen"),
            "contraindications": self.get_section(response, "Kontraindikationen"),
            "warnings": self.get_section(response, "Warnhinweise"),
            "toxicity": self.get_section(response, "Toxizität"),
            "podcast": self.get_section(response, "Podcast"),
            "literature": self.get_section(response, "Literatur"),
            "image_source": self.get_section(response, "Bildquelle"),

            "images": [
                urljoin(base, img)
                for img in response.css(".mw-parser-output img::attr(src)").getall()
            ]
        }
