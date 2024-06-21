import scrapy
from moviesscraper.items import MoviesscraperItem

class MoviesspiderSpider(scrapy.Spider):
    name = "moviesspider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse(self, response):
        # liste des éléments à scraper
        movies = response.xpath("//li[@class='ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent']")

        # je mape sur la liste des films
        for movie in movies:
            movie_url = movie.xpath(".//a/@href").get()
            yield response.follow(movie_url, callback=self.parse_movie)
        
    def parse_movie(self, response):
        item = MoviesscraperItem()

        # je procède au nettoyage des données scrapées par film
        item['title'] = response.xpath(".//h1/span/text()").get()
        item['original_title'] = response.xpath(".//div[@class='sc-d8941411-1 fTeJrK']/text()").get()
        item['score'] = response.xpath(".//span[@class='sc-bde20123-1 cMEQkK']/text()").get()
        item['gender'] = response.xpath(".//span[@class='ipc-chip__text'][1]/text()").getall()
        item['year'] = response.xpath(".//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt']/li[1]/a/text()").get()
        item['duration'] = response.xpath(".//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt']/li[3]/text()").get()
        item['description'] = response.xpath(".//section[@class='sc-1f50b7c-4 bwZAGR']//span[@role='presentation']/following-sibling::span/following-sibling::span/text()").get()
        item['actors'] = response.xpath(".//a[@class='sc-bfec09a1-1 gCQkeh']/text()").getall()
        item['director'] = response.xpath(".//span[@class='ipc-metadata-list-item__label ipc-metadata-list-item__label--btn' and text()='Réalisation']/following-sibling::div//a/text()").getall()
        item['public'] = response.xpath(".//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt']/li[2]/a/text()").get()
        item['country'] = response.xpath(".//section[@class='ipc-page-section ipc-page-section--base celwidget'][9]//div[@class='sc-f65f65be-0 bBlII']//li[2]//a/text()").get()
        item['language'] = response.xpath(".//section[@class='ipc-page-section ipc-page-section--base celwidget'][9]//div[@class='sc-f65f65be-0 bBlII']//li[4]//a/text()").get()

        yield item