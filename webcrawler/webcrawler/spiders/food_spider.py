import scrapy

class GoodFoodSpider(scrapy.Spider):
    name = "food_spider"

    #this is the list of ingredients
    ingredient_list = ["chicken"] #placeholder for parameter input

    start_urls = []
    url = 'https://www.bbcgoodfood.com/search/recipes?q='
    if ingredient_list is not None:
        for ingredient in ingredient_list:
            start_urls.append(url + ingredient)
            
    def parse(self, response):
        y = {
            'url': [],
            'title': []
        }
        for meal in response.css('h4.heading-4.standard-card-new__display-title'):
            y['url'].append(meal.css("a::attr('href')").get())
            y['title'].append(meal.css('a::text').get())

        ingredient = response.url.replace("https://www.bbcgoodfood.com/search/recipes?q=", '')

        for i in range(len(y['url'])):
            yield scrapy.Request("https://www.bbcgoodfood.com" + y['url'][i], self.parse_meal,
                                 cb_kwargs=dict(title=y['title'][i], ingredient=ingredient))
            

    def parse_meal(self, response, title, ingredient):
        recipe = response.css("div.recipe-template__instructions li.pb-xxs.pt-xxs.list-item.list-item--separator ::text").getall()
        yield { "title": title,
                "ingredient": ingredient,
                "url": response.url,
                "recipe": recipe
        }

#rip old quote spider
"""
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
"""