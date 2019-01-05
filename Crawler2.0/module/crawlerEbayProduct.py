import dbconnection.dbProductEbay as dbProductEbay
import dbconnection.dbStoretEbay as dbStoretEbay
import dbconnection.dbConnection as dbConnection
import lib.FunctionHelper as FunctionHelper
import attributes.productEbay as ProductEbay

# Get TShirt
import scrapy
import mysql.connector


class CrawlerSpiderProduct(scrapy.Spider):
    name = 'crawlerProduct'
    allowed_domains = ['ebay.com']
    type = 'T-SHIRTS'
    type_scrapy = {
        'T-SHIRTS': "/T-Shirts/15687",
        }
    custom_settings = {
        # Settings for test
        'DEV_MODE': False,
        'IS_CRAWL_NEXT_PAGE': True,  # Crawl next page in results page
        'MAX_CATEGORIES_PER_PAGE': 1,  # All: None
        'ITEMS_PER_RESULT_PAGE': None,  # Max items in results page
    }
    def __init__(self):
        self.cursor = dbConnection.connect()
    def start_requests(self):
        print('Start:...................')

        listStore = dbStoretEbay.getAllStore(self.cursor)

        for name_shop in listStore:
            print(name_shop[0])
            start_url = 'https://www.ebay.com/sch' + str(
                self.type_scrapy[self.type]) + '/m.html?_nkw=&_armrs=1&_from=&_ssn=' + str(name_shop[0]) + '&_sop=10&rt=nc&_ipg=50'
            print(start_url)
            # yield scrapy.Request(url=start_url, callback=self.parse_category,
            #                      meta={'name_shop': name_shop[0], 'page_number': 1})

    def parse(self, response):
        pass

    def parse_category(self, response):
        self.log('I just visited: ' + response.url)
        if response.css('h3.lvtitle'):
            for quote in response.css('h3.lvtitle'):
                linkProduct = quote.css('a::attr(href)')[0].extract()
                linkProduct = response.urljoin(linkProduct)
                yield scrapy.Request(url=linkProduct, callback=self.parse_product,
                                     meta={'name_shop': response.meta['name_shop']})

            #NextPage
            item = {'a': response.css('td.pagn-next').extract()}
            yield item
            nextPageUrl = response.css('td.pagn-next').css('a::attr(href)')[0].extract()
            if nextPageUrl and response.meta['page_number'] < 6:
                # nextPageUrl = response.css('td.pagn-next').css('a::attr(href)')[0].extract()
                print(nextPageUrl)
                print('page_number' + str(response.meta['page_number']))
                link = response.urljoin(nextPageUrl)
                yield scrapy.Request(url=link, callback=self.parse_category,
                                     meta={'name_shop': response.meta['name_shop'],
                                           'page_number': response.meta['page_number'] + 1})
                print("end change")
            else:
                print('No page can be next')
        else:
            print('Store has no product')
            print("""UPDATE `stores_ebay_source`
                                           SET `count_products` = -1 WHERE `stores_ebay_source`.`source_store` = '""" + str(
                response.meta['name_shop']) + """';""")
            self.cursor.execute("""UPDATE `stores_ebay_source`
                                           SET `count_products` = -1 WHERE `stores_ebay_source`.`source_store` = '""" + str(
                response.meta['name_shop']) + """';""")

            self.connection.commit()

    def parse_product(self, response):
        print('parse_product')

