"""
Analyzes submissions and posts that are deemed "recipes".
"""

from praw import objects
from fuzzywuzzy import fuzz
import string
import re

ingredients_terms = ['ingredients', 'ingredient', 'shopping list']
instructions_terms = ['instructions', 'instruction', 'method', 'directions']

# First element in each value is the fuzz ratio
recipe_titles = {}

with open('../misc/recipe_titles.txt') as titles:
    lines = titles.readlines()
    for line in lines:
        recipe_titles[line[:-1]] = 0


def determine_title(post):
    """Analyze the post and determine a suitable recipe title.

    :param post The post to analyze.
    """

    post_title = ''

    if isinstance(post, objects.Submission):
        post_title = post.title
        post_text = post.selftext
    else:  # Comment
        post_text = post.body

    text_to_analyze = ' '.join((post_title, post_text))

    for key in recipe_titles:
        # Used token set ratio to block out noise within the post.
        token_set_ratio = fuzz.token_set_ratio(key, text_to_analyze)
        recipe_titles[key] = token_set_ratio

    title = max(recipe_titles, key=recipe_titles.get)

    return title


def get_ingredients(content):
    """Analyze the contents of a post and get the list of ingredients.

    :param content The post to analyze.
    """

    ingredients = []

    lines = content.split('\n')
    for line_num, line in enumerate(lines):
        if clean_up(line) in ingredients_terms:
            for ingredient_line in lines[line_num + 1:]:
                if clean_up(ingredient_line) not in instructions_terms:
                    ingredients.append('- ' + ingredient_line)
                else:
                    break
            break

    ingredients = clean_list(ingredients)

    return ingredients


def get_instructions(content):
    """Analyze the contents of a post and get the set of instructions.

    :param content The post to analyze.
    """

    instructions = []

    lines = content.split('\n')
    for line_num, line in enumerate(lines):
        if clean_up(line) in instructions_terms:
            for instruction_line in lines[line_num + 1:]:
                instructions.append('- ' + instruction_line)
            break

    instructions = clean_list(instructions)

    return instructions


def determine_if_recipe(content):
    """Analyze the contents of a post and get the set of instructions.

    :param content The post to analyze.
    """

    lines = content.split('\n')
    has_ingredients = any(line in ingredients_terms for line in lines)
    has_instructions = any(line in instructions_terms for line in lines)

    return has_ingredients and has_instructions


def determine_type(post):
    """Analyze the post and determine a suitable recipe type.
    e.g. Breakfast, Lunch, Dinner.

    :param post: The post to analyze.
    """

    post = post.split()
    post = clean_list(post)

    breakfast_terms = ['breakfast', 'morning', 'wake up']
    lunch_terms = ['lunch', 'afternoon', 'break']
    dinner_terms = ['dinner', 'night', 'sleep', 'family dinner', 'supper']

    type_dict = {'Breakfast': 0, 'Lunch': 0, 'Dinner': 0}

    for word in post:
        if word in breakfast_terms:
            type_dict['Breakfast'] += 1
        elif word in lunch_terms:
            type_dict['Lunch'] += 1
        elif word in dinner_terms:
            type_dict['Dinner'] += 1

    recipe_type = max(type_dict, key=type_dict.get)

    if type_dict[recipe_type] == 0:
        recipe_type = 'All meals!'

    return recipe_type


def clean_up(text):
    """
    Formats the body of text to remove extraneous formatting for easier
    analysis.

    :param text: The body of text to modify and remove unecessary
    formatting
    :return: A clean body of text.
    """

    regex = re.compile('[%s]' % re.escape(string.punctuation))
    clean_text = regex.sub('', text)
    return clean_text.lower()


def clean_list(list_object):
    """Simply deletes any empty strings from a list and returns it.

    :param list_object: The list to clean up.
    :return: A clean version of the list.
    """

    return [item for item in list_object if item and
            # TODO replace with regex
            item != '- ' and item != '-  ' and item != ' ']
