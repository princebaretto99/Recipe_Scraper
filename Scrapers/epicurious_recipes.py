import html
import urllib
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
import json

def quick_save(site_str, recipes):
    save_recipes(
        path.join(config.path_data, 'recipes_raw_{}.json'.format(site_str)),
        recipes)

base_url = 'https://www.epicurious.com/search?content=recipe&page='
prefix_url = 'https://www.epicurious.com'

recipe_titles = []
recipe_img_links = []
recipe_ingredients = []
recipe_intructions = []
feeds = []

with open("dataset_epi.json", mode='w', encoding='utf-8') as f:
    json.dump([], f)

recipe_count = 1

for i in range(3, 2032):
    
    print("Page "+str(i)+" scraping started!!!")
    
    url = base_url + str(i)
    req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage,"html.parser")
    
    recipe_links_on_page = []
    
    recipe_links = page_soup.find_all('h4', {'class': 'hed'})
    
    for link in recipe_links:
        recipe_links_on_page.append(prefix_url + link.find('a')['href'])

    print(f"Total links in this Page are : {len(recipe_links_on_page)}")
        
    for recipe_url in recipe_links_on_page:
        try :
            req_recipe = Request(recipe_url, headers={'User-Agent':'Mozilla/5.0'})
            webpage_recipe = urlopen(req_recipe).read()
            page_soup_recipe = soup(webpage_recipe,"html.parser")
            
            # Name of Recipe
            name = page_soup_recipe.find('h1',itemprop="name").text
            recipe_titles.append(name)
            
            
            # Ingredients
            ingredients = page_soup_recipe.find('div',class_='ingredients-info').find('ol', class_='ingredient-groups').find_all('li', {'class':'ingredient'})
            
            temp_ingredients = []
            
            for ingredient in ingredients:
                temp_ingredients.append(ingredient.text.strip())
            
            recipe_ingredients.append(temp_ingredients)
            
            # Recipe
            recipes = page_soup_recipe.find('div',class_='instructions').find('ol', class_='preparation-groups').find_all('li', {'class':'preparation-step'})
            
            temp_recipe = []
            
            for recipe in recipes:
                temp_recipe.append(recipe.text.strip())
            
            recipe_intructions.append(temp_recipe)
        
            # Image 
            temp_img = page_soup_recipe.find('div',class_='social-img').find('img')['srcset']
            recipe_img_links.append(temp_img)

            with open("../Datasets/dataset_epi.json", mode='w', encoding='utf-8') as feedsjson:
                entry = {'Recipe_number': recipe_count,'Recipe_name': name, 'Recipe_ingredients': temp_ingredients, "Recipe_instructions": temp_recipe,"Recipe_img_link" :temp_img}
                feeds.append(entry)
                json.dump(feeds, feedsjson)

            
            
            print("Recipe "+str(recipe_count)+" Scrapped")
            recipe_count += 1
        except Exception as e:
            print("Couldnt Parse this recipe..")
            print(e)
            continue
            
    dataset_epi = pd.DataFrame(list(zip(recipe_titles, recipe_ingredients, recipe_intructions, recipe_img_links)), 
                columns =['Recipe_name', 'Recipe_ingredients', 'Recipe_instructions', 'Recipe_img_link'])

    dataset_epi.to_csv(f'../Datasets/dataset_epi_{i}.csv')
    print("Page "+str(i)+" Scraped!!!")
        
# dataset_ar = pd.DataFrame(list(zip(recipe_titles, recipe_ingredients, recipe_intructions, recipe_img_links)), 
#                columns =['Recipe_name', 'Recipe_ingredients', 'Recipe_instructions', 'Recipe_img_link'])

# dataset_ar.to_csv('../Datasets/dataset_epi.csv')