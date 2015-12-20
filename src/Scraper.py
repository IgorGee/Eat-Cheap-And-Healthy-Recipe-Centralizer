"""Analyzes posts to determine whether they are considered recipes."""

from time import time, sleep
from datetime import datetime
import praw
from src.Recipe import Recipe, PostInfo, RefinedPost
from src.RecipeHandler import RecipeHandler
from src import Analyzer

DAY_SECONDS = 24 * 3600


class RedditAPI:
    """The Reddit API."""

    def __init__(self):
        self.reddit = praw.Reddit('ECAH Scraper by /u/ECAH_Scraper')
        self.subreddit = self.reddit.get_subreddit('EatCheapAndHealthy')
        self.old_submission_ids = []
        self.fill_old_submissions()
        self.recipe_handler = RecipeHandler()
        while True:
            try:
                self.run_bot()
                if datetime.now().isoweekday() == 1:  # Monday
                    self.recipe_handler.post_weekly()
                self.go_sleep(DAY_SECONDS)
            except praw.errors.HTTPException:
                print("Server is down! Gonna sleep for 30 mins til things are "
                      "fixed up!")
                self.go_sleep(1800)

    def fill_old_submissions(self):
        """Retrieves old submissions stored.

        Used in case of Reddit's servers going down.
        """
        with open('../misc/submission_IDs.txt') as submissions_list:
            for line in submissions_list.readlines():
                line = line[:-1]
                self.old_submission_ids.append(line)

    def run_bot(self):
        """Runs the script endlessly."""

        print("Working...")
        submissions = self.get_submissions()
        for submission in submissions:
            if submission.id not in self.old_submission_ids and \
                    int(time()) - submission.created > DAY_SECONDS:
                try:
                    self.check_post(submission)
                except AttributeError:
                    pass
                comments = self.get_comments(submission)
                for comment in comments:
                    try:
                        self.check_post(comment)
                    except AttributeError:
                        pass
                self.add_checked_submission(submission.id)

    def get_submissions(self):
        """Retrieves a set of new submissions that are older than 1 day."""

        return self.subreddit.get_hot(limit=None)

    def get_comments(self, submission):
        """Retrieves a set of comments pertaining to a submission.

        :param submission: The submission to get the comments from.
        """

        submission.replace_more_comments(limit=None, threshold=0)
        all_comments = praw.helpers.flatten_tree(submission.comments)
        return all_comments

    def go_sleep(self, length_time):
        """Puts the program to sleep for a set amount of time.

        :param length_time: The amount of time the program should sleep.
        """

        print("Sleeping for", length_time, "seconds")
        sleep(length_time)

    def is_recipe(self, content):
        """
        Calls Analyzer method to check if a body of text has the qualities of a
        recipe.

        :param content: The body of text to analyze.
        """

        return Analyzer.determine_if_recipe(content)

    def check_post(self, post):
        """Checks a post for qualities of a recipe.

        :param post: The post to get the comments from.
        """

        if isinstance(post, praw.objects.Submission):
            content = post.selftext
            url = post.permalink
        else:  # Comment
            content = post.body
            submission_id = post.link_id[3:]
            parent_post = self.reddit.get_submission(
                submission_id=submission_id)
            url = parent_post.permalink + post.id

        clean_content = Analyzer.clean_up(content)

        if self.is_recipe(clean_content):
            print("Got a recipe!! Mama mia! " + str(datetime.now()))
            all_text = self.get_all_text(post)

            author = post.author.name
            karma = post.score
            date_posted = post.created
            post_id = post.id

            title = Analyzer.determine_title(post)
            ingredients = Analyzer.get_ingredients(content)
            instructions = Analyzer.get_instructions(content)
            recipe_type = Analyzer.determine_type(all_text)

            post_info = PostInfo(author, karma, date_posted, post_id, url)
            refined_post = RefinedPost(title, ingredients, instructions,
                                       recipe_type)
            recipe = Recipe(post_info, refined_post)
            self.recipe_handler.add(recipe)

    def add_checked_submission(self, submission_id):
        """
        Records a submission id when it was already scanned to prevent the
        bot from scanning it again.

        :param submission_id: The submission to record.
        """
        self.old_submission_ids.append(submission_id)
        with open('../misc/submission_IDs.txt', 'a') as submissions:
            submissions.write(submission_id + '\n')

    def get_all_text(self, post):
        """
        Obtain all the text of a submission, including its comments.
        If a comment is passed, its parent submission will be determined.

        :param post: The comment of submission to obtain the thread's text
        from.
        :return: A cleaned up version of all the text within the thread, ready
        for further analysis.
        """

        all_text = ''

        # Get the parent submission of a comment
        if isinstance(post, praw.objects.Comment):
            submission_id = post.link_id[3:]
            post = self.reddit.get_submission(submission_id=submission_id)

        submission_text = post.selftext
        submission_title = post.title
        ''.join((all_text, submission_title + '\n', submission_text + '\n'))
        comments = self.get_comments(post)
        for comment in comments:
            ''.join((all_text, comment.body + '\n'))

        clean_content = Analyzer.clean_up(all_text)

        return clean_content
