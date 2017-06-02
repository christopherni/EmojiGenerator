import emoji
import markovify

def collect_emojis_init(r):
	subreddit_name = "emojipasta"
	subreddit = r.subreddit(subreddit_name)

	for submission in subreddit.top('all', limit=5000):
		if submission.title:
			process_post(submission.title)
		else:
			process_post(submission.selftext)

count = 0
avg_words = 0

def process_post(text):
	count = count + 1