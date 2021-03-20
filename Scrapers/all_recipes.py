# Scraping Recipes - All Recipes
import html
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
import json 

base_url = 'https://www.allrecipes.com/recipes/?page='

recipe_titles = []
recipe_img_links = []
recipe_ingredients = []
recipe_intructions = []
recipe_nutritions = []

recipes_dict = []

recipe_count = 0

for i in range(31,100):
    
    print("Page "+str(i)+" scraping started!!!")
    
    url = base_url + str(i)
    req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage,"html.parser")
    
    recipe_links_on_page = []
    
    anchors = page_soup.find_all('a', {'class': 'tout__imageLink', 'href': True})
    for anchor in anchors:
        if(anchor['href'].startswith('/recipe')):
            recipe_links_on_page.append("https://www.allrecipes.com/"+anchor['href'])

    print(f"Total links in this Page are : {len(recipe_links_on_page)}")
        
    for recipe_url in recipe_links_on_page:
        try :
            req_recipe = Request(recipe_url, headers={'User-Agent':'Mozilla/5.0'})
            webpage_recipe = urlopen(req_recipe).read()
            page_soup_recipe = soup(webpage_recipe,"html.parser")
            
            # Name of Recipe
            name = page_soup_recipe.find('h1',class_='headline heading-content').text
            recipe_titles.append(name)
            
            # Ingredients
            ingredients = page_soup_recipe.find_all('span',class_='ingredients-item-name')
            temp_ingredients = []
            
            for ingredient in ingredients:
                temp_ingredients.append(ingredient.text.strip())
            
            recipe_ingredients.append(temp_ingredients)
            
            # Recipe 
            recipes = page_soup_recipe.find("ul", { "class" : "instructions-section" }).findAll("li", recursive=False)
            temp_recipe = []
            
            for j in range(len(recipes)):
                temp_recipe.append(recipes[j].find('p').text)
            
            recipe_intructions.append(temp_recipe)

            # Nutrition
            nutrition = page_soup_recipe.find('div',class_='partial recipe-nutrition-section').find('div',class_ ='section-body').text
            print(str(nutrition).strip())
            recipe_nutritions.append(str(nutrition).strip())
        
            # Image
            temp_img = page_soup_recipe.find("div", { "class" : "docked-sharebar-content-container" })
            temp_img = temp_img.find("div",{"class" : "image-container"})
            temp_img = temp_img.find("div")
            
            recipe_img_links.append(temp_img["data-src"])

            # Data to be written 
            dictionary ={ 
                "title" : recipe_titles[recipe_count], 
                "ingredients" : recipe_ingredients[recipe_count], 
                "instructions" : recipe_intructions[recipe_count], 
                "picture_link" : recipe_img_links[recipe_count],
                "nutrition_text" : recipe_nutritions[recipe_count]
            }

            # Adding to recipe_dict
            recipes_dict.append(dictionary)

            print("saving this page ka dicks")

            # Writing to dataset_ar.json 
            with open("../Datasets/dataset_ar.json", mode = "w",  encoding='utf-8') as outfile: 
                json.dump(recipes_dict, outfile)

            # Done with the recipe
            print("Recipe "+str(recipe_count)+" Scrapped")
            recipe_count += 1
        except Exception as e: 
            print("could not scrape this recipe...")
            print(e)

    dataset_ar = pd.DataFrame(list(zip(recipe_titles, recipe_ingredients, recipe_intructions, recipe_img_links, recipe_nutritions)), 
               columns =['title', 'ingredients', 'instructions', 'picture_link','nutrition_text'])

    dataset_ar.to_csv(f'../Datasets/dataset_all_recipes_{str(i)}.csv')
    print("Page "+str(i)+" Scraped!!!")
         
# Storing in CSV File
dataset_ar = pd.DataFrame(list(zip(recipe_titles, recipe_ingredients, recipe_intructions, recipe_img_links, recipe_nutritions)), 
               columns =['title', 'ingredients', 'instructions', 'picture_link','nutrition_text'])

dataset_ar.to_csv('../Datasets/dataset_all_recipes.csv')