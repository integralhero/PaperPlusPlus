import scrapy

class BlogSpider(scrapy.Spider):
    name = 'thesaurus'
    start_urls = ['http://www.thesaurus.com/browse/however']

    def parse(self, response):
        for href in response.css('.syn_of_syns ul li a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'word': response.css('.main-heading h1::text').extract()[0],
            'synonyms': response.css('.relevancy-block .relevancy-list ul li a span.text::text').extract(),
        }