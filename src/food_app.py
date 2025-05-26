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
from .PROJECT3.spoonacular_recipe import recipe_by_ingredients, is_valid_ingredient
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
        return gr.update(choices=[], visible=False), gr.update(visible=False), "", "", "Please enter ingredients."
    #Rejects any inputs not containing letters or commas
    if has_invalid_characters(user_input):
        return gr.update(choices=[], visible=False), gr.update(visible=False), "", "", "Only letters and commas allowed."
    #Clean any other inputs by filtering
    ingredients = filtered_input(user_input)
    #Rejects blank inputs & ensures there are at least two ingredients
    if not ingredients or len(ingredients.split(',')) < 2:
        return gr.update(choices=[], visible=False), gr.update(visible=False), "", "", "Enter at least two valid ingredients."

    ingredients_list = ingredients.split(',')
    invalid_items = [item for item in ingredients_list if not is_valid_ingredient(item)]
    if invalid_items:
        return gr.update(choices=[], visible=False), gr.update(visible=False), "", "", f"Invalid ingredients: {', '.join(invalid_items)}."
    #Recipe list is fetched from the Spoonacular API
    recipes = recipe_by_ingredients(ingredients)

    if not recipes or isinstance(recipes, str):
        return gr.update(choices=[], visible=False), gr.update(visible=False), "", "", "No recipes found."

    return gr.update(choices=recipes, visible=True), gr.update(visible=True), "", "", "Select a recipe to customize."

def customize_selected_recipe(recipe_title, user_input):
    #Uses llama3 to customize the selected recipe based on ingredients.
    if not recipe_title:
        return "", "Please select a recipe to customize."
    ingredients = filtered_input(user_input)
    try:
        ai_recipe = llama_recipe(recipe_title, ingredients)
        return (
    gr.update(value=f"Base Recipe: {recipe_title}", visible=True),
    gr.update(value=ai_recipe, visible=True),
    "Recipe successfully customized."
    )
    except Exception as e:
        return "", "", f"An error occurred while generating the recipe: {str(e)}"


#Creating the interface
with gr.Blocks() as food_interface:
    gr.Markdown("# 🍲 Custom Food Recipe Generator: Pick and Customize a Recipe")

    with gr.Row():
        ingredient_input = gr.Textbox(label="Enter ingredients", placeholder="e.g. beef, pasta, onion, garlic", lines=3)
        find_button = gr.Button("Find Recipes")

    recipe_dropdown = gr.Dropdown(label="Select a Recipe", choices=[], visible=False)
    customize_button = gr.Button("Customize with AI", visible=False)

    base_output = gr.Textbox(label="Base Recipe", visible=False)
    ai_output = gr.Textbox(label="Modified Recipe", visible=False)
    error_box = gr.Textbox(label="Status / Errors", interactive=False)

    find_button.click(
        recipe,
        inputs=ingredient_input,
        outputs=[recipe_dropdown, customize_button, base_output, ai_output, error_box]
    )

    customize_button.click(
        customize_selected_recipe,
        inputs=[recipe_dropdown, ingredient_input],
        outputs=[base_output, ai_output, error_box]
    )

if __name__ == '__main__':
    food_interface.launch(share=True)
