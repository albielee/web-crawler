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