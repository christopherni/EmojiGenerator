# import os
import praw
import random
from subprocess import call

# Initialize Reddit instance
r = praw.Reddit('emojipasta', user_agent='emoji_pasta bot to copy titles by /u/PeachGenitals')

# Stores the top 10 text
text = [];

# Subreddit to gather posts from
subreddit_name = "emojipasta"
subreddit = r.subreddit(subreddit_name)

# Check top 10 submissions in hot
for submission in subreddit.hot(limit = 10):
	if submission.selftext:
		text.append(submission.selftext)
	else:
		text.append(submission.title)

# Choose random submission to write to emoji.txt
file = open("emoji.txt", "w", encoding='utf-8')
file.write(random.choice(text))
file.close()

# Copy emoji.txt to clipboard
call(['bash', 'copy_emoji.sh'])