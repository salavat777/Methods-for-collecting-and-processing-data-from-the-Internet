import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from castorama_ru.items import CastoramaRuItem
from scrapy.loader import ItemLoader

class ParserCastoramaRuSpider(CrawlSpider):
    name = "parser_castorama_ru"
    allowed_domains = ["castorama.ru"]
    start_urls = ["https://www.castorama.ru/tools/power-tools/cordless-drills-and-screwdrivers/"]
    # Правила скрапинга страниц с товарами из группы товаров из start_urls
    rules = (Rule(LinkExtractor(allow=('/?PAGEN',), deny=('/?arrFilter', '/catalogue/filter',)), callback="parse_item",
             follow=True),)
    #rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        self.logger.info('######################## Hi, this is an item page! %s', response.url)
        # Получение ссылок на страницу товара и переход на парсер полей товара
        products_link = response.xpath('//a[@class="product-card__name ga-product-card-name"]/@href').getall()
        for link in products_link:
            yield response.follow(link, callback=self.parse_additional_page)

    # Парсер полей товара и картинок
    def parse_additional_page(self, response):
        self.logger.info('######################## Hi, this is an parse_additional_page page! %s', response.url)
        l = ItemLoader(item=CastoramaRuItem(), response=response)
        l.add_xpath('name', '//h1/text()')
        l.add_value('url', response.url)
        l.add_xpath('price', '//div[@class="current-price"]/div/span/span/span/span/text()')
        # получаем ссылки на картинки со страницы товара
        url_images_cut = response.xpath('//span[contains(@itemprop, "image")]/@content').getall()
        # создаем полный путь к картинкам
        images_url = list(map(lambda url_image_cut: 'https://www.castorama.ru' + url_image_cut, url_images_cut))
        l.add_value('image_urls', images_url)
        return l.load_item()
        # item = {}
        # item['name'] = response.xpath('//h1/text()').get()
        # item['url'] = response.url
        # item['price'] = response.xpath('//div[@class="current-price"]/div/span/span/span/span/text()').get()
        # # получаем ссылки на картинки со страницы товара
        # url_images_cut = response.xpath('//span[contains(@itemprop, "image")]/@content').getall()
        # # создаем полный путь к картинкам
        # images_url = list(map(lambda url_image_cut: 'https://www.castorama.ru' + url_image_cut, url_images_cut))
        # item['image_urls'] = images_url
        # yield item