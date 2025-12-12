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

import scrapy
from urllib.parse import urljoin

class FlexikonAsaSpider(scrapy.Spider):
    name = "flexikon_asa_detail"
    allowed_domains = ["flexikon.doccheck.com"]
    start_urls = [
        "https://flexikon.doccheck.com/de/Acetylsalicyls%C3%A4ure"
    ]

    def extract_section(self, response, headline_text, level="h2"):
        """
        Extracts all text between a given headline (<h2> or <h3>) 
        and the next headline of the same level.
        """
        # h2 / h3 -> span.mw-headline text='...'
        xpath = f"""
        //{level}[span[@class='mw-headline' and normalize-space(text())='{headline_text}']]
        /following-sibling::*[
            preceding-sibling::{level}[1]/span[@class='mw-headline' and normalize-space(text())='{headline_text}']
        ]
        """
        nodes = response.xpath(xpath)
        # Stop at the next h2/h3 – the XPath above already does that by condition
        texts = []
        for node in nodes:
            # We don't want to accidentally run into the next headline level
            tag = node.root.tag if hasattr(node.root, "tag") else None
            if tag in ("h2", "h3"):
                break
            part = " ".join(node.xpath(".//text()").getall())
            part = " ".join(part.split())
            if part:
                texts.append(part)
        return "\n\n".join(texts) if texts else None

    def parse(self, response):
        base = "https://flexikon.doccheck.com"

        # general info
        title = response.css("h1#firstHeading::text").get()
        image_urls = response.css(".mw-parser-output img::attr(src)").getall()
        image_urls = [urljoin(base, u) for u in image_urls]

        # main sections (German headings on the page)
        definition         = self.extract_section(response, "Definition", "h2")
        history            = self.extract_section(response, "Geschichte", "h2")
        chemistry          = self.extract_section(response, "Chemie", "h2")
        mechanism          = self.extract_section(response, "Wirkmechanismus", "h2")
        mechanism_cox1     = self.extract_section(response, "Wirkung auf COX-1", "h3")
        mechanism_cox2     = self.extract_section(response, "Wirkung auf COX-2", "h3")
        pharmacokinetics   = self.extract_section(response, "Pharmakokinetik", "h2")
        indications        = self.extract_section(response, "Indikationen", "h2")
        dosage             = self.extract_section(response, "Dosierung", "h2")
        prescription       = self.extract_section(response, "Verschreibungspflicht", "h2")
        side_effects       = self.extract_section(response, "Nebenwirkungen", "h2")
        interactions       = self.extract_section(response, "Wechselwirkungen", "h2")
        contraindications  = self.extract_section(response, "Kontraindikationen", "h2")
        warnings           = self.extract_section(response, "Warnhinweise", "h2")
        toxicity           = self.extract_section(response, "Toxizität", "h2")
        podcast            = self.extract_section(response, "Podcast", "h2")
        literature         = self.extract_section(response, "Literatur", "h2")
        image_source       = self.extract_section(response, "Bildquelle", "h2")

        yield {
            "source": "flexikon",
            "url": response.url,
            "title": title,
            "definition": definition,
            "history": history,
            "chemistry": chemistry,
            "mechanism_of_action": mechanism,
            "mechanism_cox1": mechanism_cox1,
            "mechanism_cox2": mechanism_cox2,
            "pharmacokinetics": pharmacokinetics,
            "indications": indications,
            "dosage": dosage,
            "prescription_requirement": prescription,
            "side_effects": side_effects,
            "interactions": interactions,
            "contraindications": contraindications,
            "warnings": warnings,
            "toxicity": toxicity,
            "podcast": podcast,
            "literature": literature,
            "image_source": image_source,
            "images": image_urls,
        }
