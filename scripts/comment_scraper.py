import praw
import pandas
import datetime
import json
import re

# Read from stories and slurs json files.
with open('../data/stories.json') as stories_json:
    stories_data = json.load(stories_json)
    stories_data = stories_data['stories']

with open('../data/slurs.json') as slurs_json:
    slurs_data = json.load(slurs_json)
    slurs_data = slurs_data['slurs']

reddit = praw.Reddit(client_id='VDczLkMdXSQQdQ', \
                     client_secret='z1bRECrJer5qe_cGXu_Nf94xTcY', \
                     user_agent='py:scraper')

# Create the dictionary for storing each slur-containing comment.
comment_dict = { "title": [], "score": [], "id": [], "body": [], "slurs": []}
# Create the dictionary for storing each slur's usage information.
slur_use_dict = {"id": [], "slur_used": [], "slur_category": []}
# Create the dictionary for storing each thread's slur tally.
thread_dict = {"title": [], "slurs_used": [], "category": []}

# Analyze each story.
for story in stories_data:
    submission = reddit.submission(url=story['url'])
    submission.comments.replace_more(limit=0)
    submission_slur_count = 0
    # Add basic info about each comment to the dictionary, if there are slurs in the comment.
    for comment in submission.comments.list():
        # Check each comment for slurs.
        slur_count = 0
        for slur in slurs_data:
            if slur['term'] in comment.body:
                slur_count = slur_count + 1
                submission_slur_count = submission_slur_count + 1
                slur_use_dict['id'].append(comment.id)
                slur_use_dict['slur_used'].append(slur['term'])
                slur_use_dict['slur_category'].append(slur['category'])
        # Only add a comment to the dictionary if it contains at least one slur.
        if slur_count > 0:
            comment_dict['title'].append(comment.submission.title)
            comment_dict['score'].append(comment.score)
            comment_dict['id'].append(comment.id)
            comment_dict['body'].append(comment.body)
            comment_dict['slurs'].append(slur_count)
    thread_dict['title'].append(submission.title)
    thread_dict['slurs_used'].append(submission_slur_count)
    thread_dict['category'].append(story['category'])


# Export all of the data!
comment_data = pandas.DataFrame(comment_dict)
comment_data.to_csv('../data/comments.csv', index=False)

slur_use_data = pandas.DataFrame(slur_use_dict)
slur_use_data.to_csv('../data/slurs.csv', index=False)
        