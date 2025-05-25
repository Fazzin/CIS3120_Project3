'''
This module creates an interface using gradio that generates custom food recipes based on the user's provided ingredients

Three functions
1) filtered_input function filters the input by alphabetical characters and lowers all cases
Ex: "onions! -> onions" "garlic, &milk" - > "garlic,milk" "onions123" -> "onions" etc..
2) has_invalid_characters function returns True if there are any invalid characters (e.g., symbols, digits)
3) recipe function is the main function that validates, filters, and processes the ingredient input. It fetches the base recipe
from the Spoonacular API and customizes it using the llama3 model
'''
import gradio as gr
import re
from .spoonacular_recipe import recipe_by_ingredients, is_valid_ingredient
from .ai_recipe import llama_recipe

#Filtering any bad inputs
def filtered_input(user_input):
    clean_input = []
    for item in user_input.split(','):
        #Using regex to filter only alphabetical characters and spaces. Also removes any spaces and lowers all cases
        filtered = re.sub(r'[^a-zA-Z\s]', '', item)
        filtered = filtered.strip().lower()
        if filtered:
            clean_input.append(filtered)
    return ','.join(clean_input)
    
#Checks for any invalid characters
def has_invalid_characters(text):
    for char in text:
        #If not an alphabetical letter, space, or comma, then it is an invalid character
        if not (char.isalpha() or char.isspace() or char == ','):
            return True
    return False

#Generating recipe    
def recipe(user_input):
    #Rejects any blank inputs
    if not user_input.strip():
        return 'Please enter ingredients', None
    #Rejects any inputs not containing letters or commas
    if has_invalid_characters(user_input):
        return 'Please use letters and commas only', None
    #Clean any other inputs by filtering
    ingredients = filtered_input(user_input)
    #Rejects blank inputs
    if not ingredients:
        return 'Enter valid ingredients', None
    #Ensures there are at least two ingredients
    if len(ingredients.split(',')) < 2:
        return 'Please enter at least two valid ingredients (e.g., onion, garlic)', None
    
    ingredients_list = ingredients.split(',')
    invalid_items = [item for item in ingredients_list if not is_valid_ingredient(item)]
    if invalid_items:
        return f'The following ingredients are not recognized by Spoonacular API: {', '.join(invalid_items)}', None
    #Recipe list is fetched from the Spoonacular API
    recipes = recipe_by_ingredients(ingredients)

    #Handles any errors or no results 
    if not recipes or isinstance(recipes, str) or f'{ingredients} are not valid ingredients' in recipes[0].lower() or 'error' in recipes[0].lower():
        return f"Base Recipe: {recipes[0] if isinstance(recipes, list) else recipes}", ""

    base_recipe = recipes[0]
    customized_recipe = llama_recipe(base_recipe, ingredients)
    return f'Base Recipe: {base_recipe}', customized_recipe


#Creating the interface
food_interface = gr.Interface(
    fn = recipe,
    inputs = gr.Textbox(lines = 3, label = 'Enter your ingredients (includes commas)', placeholder='e.g., onion, garlic, milk'),
    outputs = [gr.Textbox(label='Base Recipe'), gr.Textbox(label='Modified Recipe')],
    title = 'Custom Food Recipe Generator', #Interface title
    description = 'Creates recipes based on the ingredients then AI customizes it by adding variations or additional ingredients' #Interface description
)

if __name__ == '__main__':
    food_interface.launch(share=True)