# Inspiration from https://github.com/Deimos/SubredditSimulator

import emoji
import markovify
import praw
from subprocess import call

MAX_OVERLAP_RATIO = 0.5
MAX_OVERLAP_TOTAL = 10

r = praw.Reddit('emojipasta', user_agent='emoji_pasta bot to copy titles by /u/PeachGenitals')
subreddit_name = "emojipasta"
subreddit = r.subreddit(subreddit_name)

text = ""


def sentencify(text):
	text = text.strip()
	if not text.endswith((".", "?", "!")):
		text += "."
	return text

def scrape_emojis():
	global text
	for submission in subreddit.top('all', limit=5000):
		if not submission.selftext:
			text = text + sentencify(submission.title)
		else:
			text = text + sentencify(submission.selftext)

class EmojiText(markovify.Text):
	"""Markov chain to create emoji pasta scraped from reddit.com/r/emojipasta"""

	def _isemoji(self, char):
		"""Determines if char is an emoji"""
		return char in emoji.UNICODE_EMOJI

	# Accept all emoji pastas
	def test_sentence_input(self, sentence):
		return True

try:
	model = open("model.txt", "r", encoding='utf-8')
	emoji_model = EmojiText.from_json(model.read())
except FileNotFoundError:
	scrape_emojis()
	emoji_model = EmojiText(text)
	model = open("model.txt", "w", encoding='utf-8')
	model.write(emoji_model.to_json())
finally:
	model.close()

# Choose random submission to write to emoji.txt
file = open("emoji.txt", "w", encoding='utf-8')
file.write(emoji_model.make_sentence())
file.close()

# Copy emoji.txt to clipboard
call(['bash', 'copy_emoji.sh'])