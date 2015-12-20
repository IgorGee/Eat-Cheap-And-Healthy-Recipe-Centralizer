"""Eat Cheap and Healthy Scraper.

Scraper that searches through posts within ECAH for recipes and stores them in
a database.
"""

from src.DatabaseUtil import Database
from src.DriveAPI import DriveClient
from time import time, strftime, gmtime

DAY_IN_SECONDS = 86400
WEEK_IN_SECONDS = 604800 + DAY_IN_SECONDS  # 8 days ago


class RecipeHandler:
    """
    Medium class that takes incoming recipes and stores them into a database.
    """

    def __init__(self):
        self.recipe_list = []
        self.db = Database()
        self.drive = DriveClient()

    def add(self, recipe):
        """
        Appends a recipe to the queue of recipes waiting to be stored into
        a database

        :param recipe The recipe to add.
        """

        self.recipe_list.append(recipe)
        self.manage_queue()

    def manage_queue(self):
        """
        Takes all the recipes within the queue and stores them in the
        database.
        """

        while len(self.recipe_list) > 0:
            recipe = self.recipe_list.pop()
            self.db.add(recipe)

    def post_weekly(self):
        """
        Gets last weeks recipes, writes them to a file in descending order of
        karma points, and posts that file to a Google Drive doc.
        """

        recipes = self.db.get_last_weeks_recipes()
        recipes.sort(key=lambda recipe_item: recipe_item.karma, reverse=True)

        path = '../misc/document.txt'

        with open(path, 'w') as weekly_doc:
            endline = '\n' + '-' * 124 + '\n\n'
            for recipe in recipes:
                weekly_doc.write(''.join((str(recipe), endline)))

        # 7 days since yesterday
        last_week = strftime("%D", gmtime(time() - WEEK_IN_SECONDS))
        yesterday = strftime("%D", gmtime(time() - DAY_IN_SECONDS))

        self.drive.push_file(path, last_week + ' - ' + yesterday,
                             description='Top recipes for week of ' +
                                         last_week)
