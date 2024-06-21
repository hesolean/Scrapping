import scrapy
from moviesscraper.items import SeriesspiderItem


class SeriesspiderSpider(scrapy.Spider):
    name = "seriesspider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://imdb.com/chart/toptv/?ref_=nv_tvv_250"]

    def parse(self, response):
        # liste des éléments à scraper
        series = response.xpath("//li[@class='ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent']")

        # je mape sur la liste des films
        for serie in series:
            serie_url = serie.xpath(".//span[@class='ipc-metadata-list-summary-item__t']/following-sibling::div//a/@href").get()
            yield response.follow(serie_url, callback=self.parse_serie)
    
    def parse_serie(self, response):
        item = SeriesspiderItem()

        # je procède au nettoyage des données scrapées par serie
        item['title'] = response.xpath(".//h1/span/text()").get()
        item['original_title'] = response.xpath(".//h1/following-sibling::div/text()").get()
        item['score'] = response.xpath(".//span[@class='sc-bde20123-1 cMEQkK'][1]/text()").get()
        item['gender'] = response.xpath(".//section[@class='sc-b7c53eda-4 kYwFBt']//div[@class='ipc-chip-list__scroller']/a/span/text()").getall()
        item['year'] = response.xpath(".//h1/following-sibling::ul/li[2]/a/text()").get()
        item['duration'] = response.xpath(".//h1/following-sibling::ul/li[4]/text()").get()
        item['description'] = response.xpath(".//span[@class='sc-cafe919b-2 jvoyXJ']/text()").get()
        item['actors'] = response.xpath(".//a[@class='sc-bfec09a1-1 gCQkeh']/text()").getall()
        item['director'] = response.xpath(".//p[@class='sc-cafe919b-3 giURNW']/following-sibling::div/div/ul/li/div/ul/li/a/text()").getall()
        item['public'] = response.xpath(".//h1/following-sibling::ul/li[3]/a/text()").get()
        item['country'] = response.xpath(".//section[@cel_widget_id='StaticFeature_Details']//span[@class='ipc-metadata-list-item__label']/following-sibling::div//a/text()").get()
        item['language'] = response.xpath(".//section[@data-testid='Details']//li[@data-testid='title-details-languages']/div//a/text()").getall()
        item['nb_seasons'] = response.xpath(".//select[@id='browse-episodes-season']/option[2]/text()").get()
        item['nb_episodes'] = response.xpath(".//h3/span[2]/text()").get()

        yield item