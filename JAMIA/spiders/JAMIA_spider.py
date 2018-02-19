import scrapy
from JAMIA.items import JamiaItem

class JAMIASpider(scrapy.Spider):
    name = "JAMIA_spider"
    allowed_domains = ["https://www.ncbi.nlm.nih.gov/"]
    start_urls = [
        'https://www.ncbi.nlm.nih.gov/pmc/journals/76/'
    ]

    def parse(self,response):
        item = JamiaItem()
        part_urls_1 = response.xpath('//a[@class="arc-issue"]/@href').extract()
        urls_1 = []
        for each_url in part_urls_1:
            url_1 = 'https://www.ncbi.nlm.nih.gov' + each_url
            urls_1.append(url_1)
            yield scrapy.Request(url=url_1,meta={'item':item},callback=self.secound_parse,dont_filter=True)

    def secound_parse(self,response):
        item = response.meta['item']
        part_urls_2 = response.xpath('//div[@class="title"]/a/@href').extract()
        for each_url in part_urls_2:
            urls_2 = 'https://www.ncbi.nlm.nih.gov' + each_url
            yield scrapy.Request(url=urls_2,meta={'item':item},callback=self.third_parse,dont_filter=True)
        
    def third_parse(self,response):
        item = response.meta['item']
        span = response.xpath('//span[@class="cit"]')
        text = span.xpath('string(.)')[0]
        item['year'] = text.re(r'20\d\d')
        item['mounth'] = text.re(r'20\d\d (.*?);')[0]
        item['number'] = text.re(r'20\d\d .*?; (.*?):')[0]
        item['page'] = text.re(r'.*?: (\d+.\d+)')
        item['Title'] = response.xpath('//h1[@class="content-title"]/text()').extract()

        yield item
