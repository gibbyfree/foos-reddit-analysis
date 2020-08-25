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

# Create the (soon-to-be-massive) dictionary for storing each analyzed comment.
comment_dict = { "title": [], "score": [], "id": [], "body": [], "slurs": []}

# Analyze each story.
for story in stories_data:
    submission = reddit.submission(url=story['url'])
    submission.comments.replace_more(limit=0)
    # Add basic info about each comment to the dictionary.
    for comment in submission.comments.list():
        comment_dict['title'].append(comment.submission.title)
        comment_dict['score'].append(comment.score)
        comment_dict['id'].append(comment.id)
        comment_dict['body'].append(comment.body)
        # Check each comment for slurs.
        slur_count = 0
        for slur in slurs_data:
            if slur['term'] in comment.body:
                slur_count = slur_count + 1
        comment_dict['slurs'].append(slur_count)


# Export all of the data!
comment_data = pandas.DataFrame(comment_dict)
comment_data.to_csv('../data/comments.csv', index=False)
        