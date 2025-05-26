'''
Generates a variety of the given recipe using a language model (llama 3)
There are two parameters: base recipe, and ingredients
The function returns llama output based on the following requirements: 
1) Multiple variations of the recipe using the same ingredients, additional ingredients and common pantry items
2) Must include
    a) Recipe name
    b) Ingredient list
    c) Instructions
    d) Estimated time
    e) Difficulty level
'''

import ollama

def llama_recipe(recipe, ingredients):
    #llama prompt includes modified name, ingredient list, instructions, time, and difficulty level
    prompt = f'''Imagine you're a creative chef using these ingredients: {ingredients} and using this recipe, '{recipe}'
    Have multiple variations of the recipe using the same ingredients, additional ingredients, and common pantry items
    This should be a customization of the recipe or suggestive creative variations
    Must include: 
    
New modified recipe name
Ingredient list
Step-by-step cooking instructions,
Estimated time,
Difficulty level,
'''
try:#Gets a response from the llama3 model 
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])#Returns actual generated text from llama model
    return response['message']['content']
except Exception as e:
    return f'Error: {str(e)}'
