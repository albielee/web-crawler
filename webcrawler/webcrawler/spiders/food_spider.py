import scrapy

class GoodFoodSpider(scrapy.Spider):
    name = "food_spider"

    #this is the list of ingredients
    ingredient_list = ["chicken"] #placeholder for parameter input

    start_urls = []
    url = 'https://www.bbcgoodfood.com/search/recipes?q='
    if ingredient_list is not None:
        for i, ingredient in enumerate(ingredient_list):
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

    def recipe_refiner(self, recipe_list):
        #it is a new line if:
        #if has a number at the start
        #a fraction at the start
        #a few
        #handful
        #other measurements
        #x, to serve
        measurements = ['tsp ','tbsp ','g ','kg ','grams ','gram ']
        values = ['1','2','3','4','5','6','7','8','9','0','½','¼','¾','handful',
                'a pinch','a few','a couple','a bunch']
        all_possible_ingredient = ['onion','olive oil','garlic cloves','chilli flakes','chopped tomatoes','caster sugar','penne','cheddar','chicken breast']
        #recipe should be an array of tuples (ingredient, value, measurement), e.g. (oliveoil, 2, tsp)
        def contains_return(input_string, values):
            for val in values:
                if(val in input_string):
                    return val
            return None
        def contains_bool(input_string, values):
            for val in values:
                if(val in input_string):
                    return True
            return False

        def contains_number(input_string, values):
            return ''.join(i for i in input_string if contains_bool(i, values))

        new_recipe = []
        line = ['','','']

        for item in recipe_list:
            item.replace(" ", "")

            measurement = contains_return(item, measurements)
            ingredient = contains_return(item, all_possible_ingredient)

            containing = contains_bool(item, values)
            val = contains_number(item, values)

            #if contains, so new line and if its
            if(containing):
                new_recipe.append(line)
                line = ['','','']
            if(ingredient != None):
                line[0] = ingredient
            if(val != ''):
                line[1] = val
            if(measurement != None):
                line[2] = measurement
        return new_recipe

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