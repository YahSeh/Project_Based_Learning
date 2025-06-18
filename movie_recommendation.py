import numpy as np
import random
import re
from lightfm.datasets import fetch_movielens
from lightfm import LightFM

def normalize_title(title):
    title = title.strip()

    # Extract year (e.g., "(1996)") if present
    year_match = re.search(r"\(\d{4}\)$", title)
    year = year_match.group(0) if year_match else ""
    
    # Remove year from title temporarily
    if year:
        title = title[: -len(year)].strip()

    # Move article to front if needed
    for article in ['The', 'A', 'An']:
        suffix = f", {article}"
        if title.endswith(suffix):
            main = title[:-len(suffix)].strip()
            return f"{article} {main} {year}".strip()

    # If no article moved, just append the year again
    return f"{title} {year}".strip()

def load_movie_titles(path):
    movie_titles = {}
    with open(path, encoding='ISO-8859-1') as f:
        for line in f:
            parts = line.strip().split('|')
            movie_id = int(parts[0])
            raw_title = parts[1]
            title = normalize_title(raw_title)
            movie_titles[movie_id] = title

    # Debug check for The Rock
    print("Movie ID 127 (should be 'The Rock'):", movie_titles.get(117, "Not found"))

    # Build list in LightFM’s expected order (movie ID 1 → index 0)
    return [movie_titles[i + 1] for i in range(1682)]


# Fetch data and format it
data = fetch_movielens(min_rating=4.0)

# Replace item_labels with correct full titles
data['item_labels'] = load_movie_titles('/home/yahseh/lightfm_manual/ml-100k/u.item')

# Print training and testing data
print(repr(data['train']))
print(repr(data['test']))

# Train model with WARP loss
model = LightFM(loss='warp')
model.fit(data['train'], epochs=30, num_threads=2)

def sample_recommendation(model, data, user_ids):
    n_users, n_items = data['train'].shape
    item_labels = data['item_labels']
    train = data['train'].tocsr()

    for user_id in user_ids:
        known_positives = [item_labels[i] for i in train[user_id].indices]

        scores = model.predict(user_id, np.arange(n_items))
        known_positive_indices = set(train[user_id].indices)
        unseen_indices = [i for i in np.argsort(-scores) if i not in known_positive_indices]
        top_items = [item_labels[i] for i in unseen_indices[:5]]

        print(f"User {user_id}")
        print("     Known positives:")
        for x in known_positives[:5]:
            print(f"        {normalize_title(x)}")
        print("     Recommended:")
        for x in top_items:
            print(f"        {normalize_title(x)}")

# Get total number of users from the shape of the train matrix
n_users, _ = data['train'].shape

# Select 5 random unique user IDs
random_user_ids = random.sample(range(n_users), 5)

sample_recommendation(model, data, random_user_ids)
