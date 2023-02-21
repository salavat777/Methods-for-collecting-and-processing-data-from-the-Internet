import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem

class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://krasnoyarsk.hh.ru/search/vacancy?text=Data+science&salary=&area=88&no_magic=true&ored_clusters=true&items_on_page=20&enable_snippets=true&excluded_text="
            ]

    def parse(self, response: HtmlResponse):
        print('\n#########################\n%s\n##########################\n'%response.url)
        vacancies_link = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in vacancies_link:
            yield response.follow(link, callback=self.parse_vacancy)
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_vacancy(self, response: HtmlResponse):

        vacancy_name = response.css("h1::text").get()
        vacancy_url = response.url
        vacancy_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        #print('\n#######################\n%s\n' % vacancy_salary)
        vacancy_salary_digit_list = ''.join(letter for letter in ''.join(vacancy_salary) if letter in ' \t0123456789').split()
        if len(vacancy_salary_digit_list) == 2:
            vacancy_salary_from = int(vacancy_salary_digit_list[0])
            vacancy_salary_before = int(vacancy_salary_digit_list[1])
        elif ''.join(vacancy_salary[0].split()) == 'от' and len(vacancy_salary_digit_list) == 1:
            vacancy_salary_from = int(vacancy_salary_digit_list[0])
            vacancy_salary_before = None
        elif ''.join(vacancy_salary[0].split()) == 'до' and len(vacancy_salary_digit_list) == 1:
            vacancy_salary_from = None
            vacancy_salary_before = int(vacancy_salary_digit_list[1])
        else:
            vacancy_salary_from = None
            vacancy_salary_before = None
        #print('\n#######################\n%s\n' % vacancy_salary_digit_list)
        yield ParserJobItem(name=vacancy_name, url=vacancy_url, salary_from=vacancy_salary_from, salary_before=vacancy_salary_before)
