import dbconnection.dbProductEbay as dbProductEbay
import dbconnection.dbStoretEbay as dbStoretEbay
import lib.FunctionHelper as FunctionHelper
import attributes.productEbay as ProductEbay

# Get TShirt
import scrapy
import mysql.connector


class CrawlerSpiderStore(scrapy.Spider):
    name = 'crawlerStoreEbay'
    allowed_domains = ['ebay.com']

    custom_settings = {
        # Settings for test
        'DEV_MODE': False,
        'IS_CRAWL_NEXT_PAGE': True,  # Crawl next page in results page
        'MAX_CATEGORIES_PER_PAGE': 1,  # All: None
        'ITEMS_PER_RESULT_PAGE': None,  # Max items in results page
    }
    # 'https://www.ebay.com/b/T-Shirts/15687?Brand=Gildan&Style=Basic%2520Tee&rt=nc&_sop=10',
    start_url = ['https://www.ebay.com/b/Gildan-Unisex-Adult-T-Shirts/155193/bn_14699428?rt=nc',
                 'https://www.ebay.com/b/T-Shirts/15687?Brand=Gildan&Style=Basic%2520Tee&rt=nc']

    def start_requests(self):
        print('Start:...................')

        for link in self.start_url:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_category)

    def parse_category(self, response):
        self.log('I just visited: ' + response.url)
        if response.css('li.s-item'):
            for quote in response.css('li.s-item'):
                linkProduct = quote.css('div.s-item__image > a::attr(href)')[0].extract()
                yield scrapy.Request(url=linkProduct, callback=self.parse_detail_product)
            #NextPage
            item = {'a': response.css('a[rel*=next]::attr(href)').extract()}
            nextPageUrl = response.css('a[rel*=next]::attr(href)')
            if nextPageUrl:
                nextPageUrl = response.css('a[rel*=next]::attr(href)')[0].extract()
                link = response.urljoin(nextPageUrl)
                yield scrapy.Request(url=link, callback=self.parse_category)
            else:
                print('No page can be next')
        else:
            print('No product in page!')

    def parse_detail_product(self, response):
        name = response.css('a#mbgLink>span::text').extract()
        if name:
            dbStoretEbay.insertStore(name[0])