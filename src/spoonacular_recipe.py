'''
This module retrieves recipe names from Spoonacular API based on a list of ingredients given
Two functions
is_valid_ingredient checks if an ingredient entered by the user is in the database
recipe_by_ingredients requires one parameter, ingredients (list of string)
Returns recipe names based on the ingredients
'''

import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('spoonacular_API') #Loads api key
    
#Checks if user's ingredient is in the database
def is_valid_ingredient(ingredient_name):
    url = 'https://api.spoonacular.com/food/ingredients/autocomplete'
    params = {
        'query': ingredient_name,
        'number': 1,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return False
    results = response.json()
    #Checks if the result matches with the ingredient
    return bool(results and results[0]['name'].lower() == ingredient_name.lower())

#Converts ingredient entered by user into recipes found by spoonacular's API
def recipe_by_ingredients(ingredients, max_results=5):
    #Ensures there are no whitespace or incorrect casing by stripping and lowering cases
    if isinstance(ingredients, list):
        ingredients = ','.join([item.strip().lower() for item in ingredients])
    elif isinstance(ingredients, str):
        ingredients = ','.join([i.strip().lower() for i in ingredients.split(',')])
    else:
        return ['Error: Ingredients are in invalid format']
    
    if not ingredients:
        return ['Error: No Ingredients found']
    
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'ingredients': ingredients,
        'number': max_results, #Maximum number of recipes returned (5)
        'ranking': 1,
        'apiKey': api_key
    }
    
    #Sends GET request to the API
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return [f'Error: {response.status_code} - {response.text}']

    try:
        results = response.json()
        #Extracts the recipe's title from the response
        recipe_names = [r.get('title') for r in results]
        #Returns the recipe or if there isn't one, then it isnt found
        return recipe_names or ['No recipes found!']
    except Exception as e:
        return f'Parsing error: {str(e)}'
