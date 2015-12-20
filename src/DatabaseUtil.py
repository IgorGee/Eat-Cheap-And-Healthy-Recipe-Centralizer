"""Basic CRUD and Data Analysis of Recipes"""

import sqlite3
from time import time
from src.Recipe import Recipe, PostInfo, RefinedPost


class Database:
    """Class that handles all database operations."""

    def __init__(self):
        self.connection = sqlite3.connect('../DDL Files/recipes_db.sqlite')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Creates the database if one has not been created."""

        try:
            self.cursor.execute('CREATE TABLE IF NOT EXISTS Recipes ('
                                'post_id TEXT PRIMARY KEY,'
                                'author TEXT,'
                                'karma INTEGER,'
                                'url TEXT,'
                                'title TEXT,'
                                'ingredients TEXT,'
                                'instructions TEXT,'
                                'type TEXT,'
                                'time INTEGER)')
        except sqlite3.OperationalError:
            pass

    def add(self, recipe):
        """Calls a query to add a new row to the recipe database.

        :param recipe The recipe to insert into the database.
        """

        post_id = recipe.id
        author = recipe.author
        karma = recipe.karma
        url = recipe.url
        title = recipe.title
        ingredients = self.get_csv(recipe.ingredients)
        instructions = self.get_csv(recipe.instructions)
        recipe_type = recipe.type
        time_posted = recipe.time

        sql = 'INSERT INTO Recipes VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'
        values = [post_id, author, karma, url, title, ingredients,
                  instructions, recipe_type, time_posted]
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
        except sqlite3.IntegrityError:
            print('Already recorded that recipe!')

    def get_last_weeks_recipes(self):
        """Retrieves a list of recipes from this past week"""

        recipe_list = []

        yesterday = time() - 86400
        week_from_yesterday = yesterday - 604800
        sql = 'SELECT * FROM Recipes WHERE time BETWEEN ? AND ?'
        rows = self.cursor.execute(sql, [week_from_yesterday, yesterday]
                                   ).fetchall()

        for row in rows:
            try:
                post_id = row[0]
                author = row[1]
                karma = row[2]
                url = row[3]
                title = row[4]
                ingredients = self.get_list_from_csv(row[5])
                instructions = self.get_list_from_csv(row[6])
                recipe_type = row[7]
                time_posted = row[8]

                post_info = PostInfo(author, karma, time_posted, post_id, url)
                refined_post = RefinedPost(title, ingredients, instructions,
                                           recipe_type)
                recipe = Recipe(post_info, refined_post)
                recipe_list.append(recipe)

            except TypeError:
                print('No recipes this past week!')

        return recipe_list

    def get_recipes_from_author(self, author):
        """Retrieves a list of recipes posted by a certain redditor.

        :param author: The redditor who created the recipe posts.
        :return: The recipe object.
        """

        recipe_list = []

        sql = 'SELECT * FROM Recipes WHERE author = ?'
        rows = self.cursor.execute(sql, [author]).fetchall()

        for row in rows:
            try:
                post_id = row[0]
                author = row[1]
                karma = row[2]
                url = row[3]
                title = row[4]
                ingredients = self.get_list_from_csv(row[5])
                instructions = self.get_list_from_csv(row[6])
                recipe_type = row[7]
                time_posted = row[8]

                post_info = PostInfo(author, karma, time_posted, post_id, url)
                refined_post = RefinedPost(title, ingredients, instructions,
                                           recipe_type)
                recipe = Recipe(post_info, refined_post)
                recipe_list.append(recipe)

            except TypeError:
                print(author, 'was not a valid author in the Recipes '
                              'database.')

        return recipe_list

    def get_csv(self, list_of_strings):
        """Converts a list of strings to a semi-colon separated string.

        :param list_of_strings: The list of strings to convert.
        :return: The string that was converted from the list.
        """

        return ';'.join(list_of_strings)

    def deserialize_to_recipe(self, recipe_id):
        """
        Create a recipe object from a given id.

        :param recipe_id: The specific post we wish to recreate a recipe object
        from again.
        :return: The recipe object.
        """

        sql = 'SELECT * FROM Recipes WHERE post_id = ?'
        row = self.cursor.execute(sql, [recipe_id]).fetchone()

        try:
            post_id = row[0]
            author = row[1]
            karma = row[2]
            url = row[3]
            title = row[4]
            ingredients = self.get_list_from_csv(row[5])
            instructions = self.get_list_from_csv(row[6])
            recipe_type = row[7]
            time_posted = row[8]

            post_info = PostInfo(author, karma, time_posted, post_id, url)
            refined_post = RefinedPost(title, ingredients, instructions,
                                       recipe_type)
            recipe = Recipe(post_info, refined_post)
            return recipe

        except TypeError:
            print(recipe_id, 'was not a valid entry in the Recipes database.')

    def get_list_from_csv(self, csv_of_strings):
        """
        Converts a string of semi-colon separated values into a list of
        strings.

        :param csv_of_strings: The string to convert back into a list.
        :return: The list of values from the string.
        """
        return csv_of_strings.split(';')
