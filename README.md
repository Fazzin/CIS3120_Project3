# CIS3120_Project3
## CIS 3120 Programming to Analytics Project 3
### Requires
·[Python](https://www.python.org/downloads/)  
·[Requests](https://pypi.org/project/requests/)  
·[BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)  
·[Ollama](https://ollama.com/download)  
·[python-dotenv](https://pypi.org/project/python-dotenv/)  
·[Gradio](https://www.gradio.app/guides/quickstart)  
## What does this repository do?  
This custom food recipe generator creates custom recipes based on the user's ingredients.   
It does this by getting a matching recipe from the Spoonacular API and using LLama3 to creatively customize recipes with variations  
The custom recipe provides:  
New recipe name  
Ingredient list  
Cooking instructions  
Time estimate  
Difficulty rating  
## Making sure Ollama is set up for llama3
###  Install Ollama (if not already)
https://ollama.com/download
### Pull the LLaMA model
ollama pull llama3
### Start the Ollama server
ollama run llama3
## How do I run this repository?
| 1 | Clone the repo. Git clone https://github.com/Fazzin/CIS3120_Project3.git  
| 2 | Change directory to project root. cd CIS3120_Project3  
| 3 | Ensure the requirements are fufilled: · Python · Requests · BeautifulSoup4 · Ollama · Matplotlib  
| 4 | Create a virtual environment. python -m venv gradio_venv  
| 5 | Run the virtual environment. MACOS: source gradio_venv/bin/activate | Windows: gradio_venv\Scripts\activate  
| 6 | Run the main file from the root folder. python -m src.food_app  
| 7 | Visit the custom link or locally  
