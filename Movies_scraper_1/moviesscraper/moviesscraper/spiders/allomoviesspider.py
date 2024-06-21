import scrapy
from moviesscraper.items import AllomoviesscraperItem


class AllomoviesSpider(scrapy.Spider):
    name = "allomoviesspider"
    allowed_domains = ["allocine.fr"]
    start_urls = [f"https://allocine.fr/films?page={i}" for i in range(1, 2)]    
    # j'utilise une classe hérité de la classe de base pour le nettoyage des données
    custom_settings = {'ITEM_PIPELINES' : {
   "moviesscraper.pipelines.Allo": 200,
   # "moviesscraper.pipelines.DatabasePipeline": 300,
}}

    def parse(self, response):
        # liste des éléments à scraper
        movies = response.xpath(".//li[@class='mdl']")

        # je mape sur la liste des films
        for movie in movies:
            movie_url = movie.xpath(".//a[@class='meta-title-link']/@href").get()
            yield response.follow(movie_url, callback=self.parse_movie)
        
    def parse_movie(self, response):
        item = AllomoviesscraperItem()

        # je procède au nettoyage des données scrapées par film
        item['title'] = response.xpath(".//div[@class='titlebar-title titlebar-title-xl']/text()").get(),
        item['original_title'] = response.xpath(".//div[@class='card entity-card entity-card-list cf entity-card-player-ovw']//div[@class='meta-body-item']/span[2]/text()").get(),
        item['presse_score'] = response.xpath(".//div[@class='rating-item']/div/div/span/text()").get(),
        item['viewer_score'] = response.xpath(".//div[@class='rating-item'][2]//span[@class='stareval-note']/text()").get(),
        item['gender'] = response.xpath(".//div[@class='meta-body-item meta-body-info']/span[@class='spacer'][2]/following-sibling::span/text()").getall(),
        item['year'] = response.xpath(".//section[@class='section section-wrap gd-2-cols gd-gap-30']//div[@class='meta-body-item meta-body-info']/span/text()").get(),
        item['duration'] = response.xpath("//div[@class='meta-body-item meta-body-info']/text()").getall(),
        item['description'] = response.xpath(".//p[@class='bo-p']/text()").get(),
        item['actors'] = response.xpath(".//section[@class='section ovw']//div[@class='gd gd-gap-20 gd-xs-2 gd-s-4']//a/text()").getall(),
        item['director'] = response.xpath(".//div[@class='meta-body-item meta-body-direction meta-body-oneline']/span/text()").getall(),
        item['public'] = response.xpath(".//div[@class='certificate']//span[@class='certificate-text']/text()").get(),
        item['country'] = response.xpath(".//section[@class='section ovw ovw-technical']/div[@class='item']//span[@class='that']/span/text()").get(),
        item['language'] = response.xpath(".//section[@class='section ovw ovw-technical']//span[@class='what light' and text()='Langues']/following-sibling::span/text()").get()
        
        yield item
