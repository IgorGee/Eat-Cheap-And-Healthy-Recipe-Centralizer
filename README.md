![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Language](https://img.shields.io/badge/Python-3.5-blue.svg)
![Release](https://img.shields.io/badge/Release-v1.0.0-yellow.svg)

# Eat-Cheap-And-Healthy-Recipe-Centralizer

A Reddit bot specifically for the subreddit [/r/EatCheapAndHealthy](https://www.reddit.com/r/EatCheapAndHealthy/).

It scouts through submissions and comments and analyzes each post, determining whether or not someone posted a recipe.

It also predicts the titles of the recipes utilizing Levenshtein distance measurements.

Every Monday, all posts gathered from the past week are assembled and posted to a Google Drive Document in descending order of popularity.

[Example Document](https://docs.google.com/document/d/1ot7lTm_QvE8h1uhQXKVpudD4rKXSpTfQvrrN_ahbkjw/edit)

# External Libraries Used

[PRAW](https://github.com/praw-dev/praw)

[FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy)

[Google API Python Client](https://github.com/google/google-api-python-client) (Google Drive API)

