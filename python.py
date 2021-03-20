import pandas as pd
import pickle
import numpy as np
from textblob import TextBlob

temp_data = pd.read_csv("final_full_csv.csv")
all_ingredients = set()
red_words = ["tablespoon","tablespoons","cups","cup","drops","drop","teaspoon","teaspoons","½","¼","⅔","large","%","fresh","⅓","®","¾", "4\\u2009½","⅛","1\\u2009½","1\\u2009⅓","1\\u2009¼",""]
temp_data["new_ings"] = np.nan
for j in range(len(temp_data)):

    txt = str(temp_data["ingredients"][j])

    blob = TextBlob(txt)
    nouns = blob.noun_phrases

    for i in range(len(nouns)):
        arr = nouns[i].split(" ")
        for word in arr:
            if word in red_words:
                arr.remove(word)
        
        
        nouns[i] = " ".join(arr)

    for i in range(len(nouns)):
        arr = nouns[i].split(" ")
        for word in arr:
            if word in red_words:
                arr.remove(word)
        
        if( " " in arr):
            arr.remove(" ")
        if("" in arr):
            arr.remove("")

        nouns[i] = " ".join(arr)
    
    print(f"Cleaned txt : {nouns}")

    temp_data["new_ings"][j] = nouns
    
    for phrase in nouns:
        all_ingredients.add(phrase)

print("*************************************************************************************************")
print(temp_data["new_ings"])
print("*************************************************************************************************")

print("*************************************************************************************************")
print(len(temp_data))
print("*************************************************************************************************")

print("*************************************************************************************************")
print(len(all_ingredients))
print("*************************************************************************************************")

temp_data.to_csv("ALL_RECIPES_CLEANED.CSV")

with open('all_ingredients.pickle', 'wb') as f:
    pickle.dump(all_ingredients, f)




