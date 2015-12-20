"""Container classes"""


class Recipe:
    """Concrete Recipe.

    Holds a unique recipe with the ability to display it in several ways.
    """

    def __init__(self, post_info, refined_post):
        self.author = post_info.author
        self.karma = post_info.karma
        self.time = post_info.time
        self.id = post_info.id
        self.url = post_info.link
        self.title = refined_post.title
        self.ingredients = refined_post.ingredients
        self.instructions = refined_post.instructions
        self.type = refined_post.type

    def simple_print(self):
        """
        A minimalistic display of the recipe with just the title, ingredients,
        and instructions.
        """

        print(self.title)
        print("Ingredients")
        for ingredient in self.ingredients:
            print(ingredient)
        print("Instructions")
        for instruction in self.instructions:
            print(instruction)

    def __str__(self):
        return '{0} - /u/{1}\n' \
               '{2}\n\n' \
               'Ingredients:\n\n' \
               '{3}\n\nInstructions:\n\n' \
               '{4}'.format(self.title, self.author, self.url,
                            '\n'.join(self.ingredients),
                            '\n'.join(self.instructions))

    def __repr__(self):
        return self.__str__()


class PostInfo:
    """Container for username and karma score of a post."""

    def __init__(self, username, karma, date_posted, post_id, link):
        """
        :param username: The reddit username of the original poster.
        :param karma: The net amount of points that post was scored.
        :param date_posted: The time at which this post was created.
        :param post_id: The id of the post.
        :param link: The URL link to the actual post.
        """

        self.author = username
        self.karma = karma
        self.time = date_posted
        self.id = post_id
        self.link = link


class RefinedPost:
    """Container for title, ingredients, and instructions of a recipe."""

    def __init__(self, title, ingredients, instructions, recipe_type):
        """
        :param title: The title of the recipe.
        :param ingredients: The list of ingredients for the recipe.
        :param instructions: The set of instructions for the recipe.
        :param recipe_type: The type of recipe this is.
        """

        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.type = recipe_type
