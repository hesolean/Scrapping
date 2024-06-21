# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviesscraperItem(scrapy.Item):
    
    title  = scrapy.Field()
    original_title = scrapy.Field()
    score = scrapy.Field()
    gender = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    description = scrapy.Field()
    actors = scrapy.Field()
    director = scrapy.Field()
    public = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()

class SeriesspiderItem(scrapy.Item):
    
    title  = scrapy.Field()
    original_title = scrapy.Field()
    score = scrapy.Field()
    gender = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    description = scrapy.Field()
    actors = scrapy.Field()
    director = scrapy.Field()
    public = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    nb_seasons = scrapy.Field()
    nb_episodes = scrapy.Field()

class AllomoviesscraperItem(scrapy.Item):
    title  = scrapy.Field()
    original_title = scrapy.Field()
    presse_score = scrapy.Field()
    viewer_score = scrapy.Field()
    gender = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    description = scrapy.Field()
    actors = scrapy.Field()
    director = scrapy.Field()
    public = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
