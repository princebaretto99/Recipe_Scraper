import pickle

all = set()

with open('all_ingredients.pickle', 'rb') as f:
    all = pickle.load(f)

print(all)