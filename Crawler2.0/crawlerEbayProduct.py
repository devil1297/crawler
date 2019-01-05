import dbconnection.dbProductEbay as dbProductEbay
import dbconnection.dbStoretEbay as dbStoretEbay
import lib.FunctionHelper as FunctionHelper
import attributes.productEbay as ProductEbay

# Get TShirt
import scrapy
import mysql.connector


class CrawlerSpiderProduct(scrapy.Spider):
    name = 'crawlerProduct'
    allowed_domains = ['ebay.com','picclick.com']
    type = 'T-SHIRTS'
    type_scrapy = {
        'T-SHIRTS': "/T-Shirts/15687",
        }
    storeEnd = ''
    custom_settings = {
        # Settings for test
        'DEV_MODE': False,
        'IS_CRAWL_NEXT_PAGE': True,  # Crawl next page in results page
        'MAX_CATEGORIES_PER_PAGE': 1,  # All: None
        'ITEMS_PER_RESULT_PAGE': None,  # Max items in results page
    }

    def start_requests(self):
        print('Start:...................')
        listStore = dbStoretEbay.getAllStoreNotEmpty()

        for name_shop in listStore:
            print(name_shop[0])
            start_url = 'https://www.ebay.com/sch' + str(self.type_scrapy[self.type]) + '/m.html?_nkw=&_armrs=1&_from=&_ssn=' + str(name_shop[0]) + '&_sop=10&rt=nc&_ipg=100'
            print(start_url)
            yield scrapy.Request(url=start_url, callback=self.parse_category,meta={'name_shop': name_shop[0], 'page_number': 1})
    def parse(self, response):
        pass

    def parse_category(self, response):
        self.log('I just visited: ' + response.url)
        if response.css('h3.lvtitle'):
            for quote in response.css('ul#ListViewInner > li'):
                id = str(quote.css('::attr(listingid)')[0].extract())
                title = str(quote.css('h3.lvtitle > a::attr(title)')[0].extract()).replace('Click this link to access ','').replace('"', '\'')
                [status, type_product] = FunctionHelper.get_type_product(title)
                if status == 1:
                    if quote.css('div > div > a > img::attr(imgurl)'):
                        image_link=str(quote.css('div > div > a > img::attr(imgurl)')[0].extract()).replace('225.','1600.')
                    else:
                        image_link = str(quote.css('div > div > a > img::attr(src)')[0].extract()).replace('225.', '1600.')
                    value = {'id': id,
                             'title': title,
                             'type_product': type_product,
                             'image_link': image_link,
                             'source_store': response.meta['name_shop']

                             }
                    textLink = str(quote.css('h3.lvtitle > a::attr(href)')[0].extract())
                    part = textLink.replace('https://', '').split('/')
                    linkProduct = response.urljoin('https://picclick.com/' + part[2] + '-' + str(id) + '.html')
                    yield scrapy.Request(url=linkProduct, callback=self.parse_detail_product,
                                         meta=value)

            #NextPage
            item = {'a': response.css('td.pagn-next').extract()}
            nextPageUrl = response.css('td.pagn-next').css('a::attr(href)')
            if nextPageUrl and self.storeEnd.find(response.meta['name_shop']) == -1:
                nextPageUrl = response.css('td.pagn-next').css('a::attr(href)')[0].extract()
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
            dbStoretEbay.updateEmptyStore(response.meta['name_shop'])
            print('Store has no product')


    def parse_product(self, response):
        # print('View........' + response.url)
        product = response.css('ul.items > li > a::attr(href)')
        if product:
            detail_product = str(response.css('ul.items > li > a::attr(href)')[0].extract())
            linkProduct = response.urljoin('https://picclick.com' + detail_product)
            yield scrapy.Request(url=linkProduct, callback=self.parse_detail_product,
                                 meta=response.meta)
        else:
            pass

    def parse_detail_product(self, response):
        item = {'a':response.css('ul.insights > li').css('span#hitcount::text')[0].extract(),
                'c': response.css('ul.insights > div#morepopularity').css('div.modal-body > p::text')[1].extract()}

        value = response.meta
        value['sold_ebay'] = FunctionHelper.getSoldProductEbay(item['c'])
        value['created_date'] = FunctionHelper.getDayProductEbay(item['c'])
        value['view_ebay'] = FunctionHelper.getViewProductEbay(item['a'])
        if value['created_date'] < 60 and value['created_date'] > 7 :
            dbProductEbay.insertProduct(value['id'],value['title'] ,value['image_link'] ,value['type_product'] ,value['source_store'] ,value['sold_ebay'] ,value['created_date'] ,value['view_ebay'] )
        else:
            self.storeEnd += (',' + str(value['source_store']))