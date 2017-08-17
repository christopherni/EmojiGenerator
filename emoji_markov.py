# Inspiration from https://github.com/Deimos/SubredditSimulator

from datetime import datetime, timedelta
import emoji
from emoji_generator import EmojiGenerator
import json
import markovify
import praw
import random
import re
from subprocess import call
import sys

r = praw.Reddit('emojipasta', user_agent='emoji_pasta bot to generate titles by /u/PeachGenitals')
subreddit_name = "emojipasta"
subreddit = r.subreddit(subreddit_name)

text = ""

def is_emoji(char):
	"""Determines if char is an emoji"""
	return char in emoji.UNICODE_EMOJI

emoji_count = 0
num_words = 0

def sentencify(text):
	global emoji_count
	text = text.strip()
	modified_text = ""
	if not text.endswith((".", "?", "!")):
		text += "."
	for c in text:
		if not is_emoji(c):
			modified_text = modified_text + c
		# else:
		# 	emoji_count = emoji_count + 1
	return modified_text

def scrape_emojis(submission, num):
	global text
	for submission in subreddit.top(submission, limit=num):
		if not submission.selftext:
			text = text + sentencify(submission.title)
		else:
			text = text + sentencify(submission.selftext)

class EmojiText(markovify.Text):
	"""Markov chain to create emoji pasta scraped from reddit.com/r/emojipasta"""

	DEFAULT_MAX_OVERLAP_RATIO = 0.5
	DEFAULT_MAX_OVERLAP_TOTAL = 10

	# def word_split(self, sentence):
	# 	global num_words
	# 	temp = re.split(self.word_split_pattern, sentence)
	# 	num_words = num_words + len(temp)
	# 	return temp

	# Accept all emoji pastas
	def test_sentence_input(self, sentence):
		return True

# Check if it has been 24 hours since last train.
def check_time():
	try:
		file = open("info.txt", "r")
		date_string = file.read()
		last_train = datetime.strptime(date_string, '%c')
		diff = datetime.now() - last_train
		file.close()
		return diff.days > 0
	except FileNotFoundError:
		return True

try:
	model = open("json/model.json", "r", encoding='utf-8')
	emoji_model = EmojiText.from_json(model.read())
	if len(sys.argv) > 1 and check_time():
		file = open("info.txt", "w")
		file.write(datetime.now().strftime('%c'))
		file.close()
		scrape_emojis('day', 20)
	params = json.load(open('json/emoji_params.json', 'r',))
	emoji_count = params['emoji_count']
	num_words = params['num_words']
except FileNotFoundError:
	scrape_emojis('all', 5000)
	emoji_model = EmojiText(text)
	model = open("json/model.json", "w", encoding='utf-8')
	model.write(emoji_model.to_json())
finally:
	model.close()

# Choose random submission to write to emoji.txt
file = open("emoji.txt", "w", encoding='utf-8')
avg_words = num_words / 5000
avg_emojs = emoji_count / 5000
res = ""
probability_word = 1.2
probability_emoji = 1.2

# Scales probability down as word length approachs average length
while random.random() < probability_word:
	res = res + emoji_model.make_sentence()
	probability_word = 1.2 - len(res.split()) / avg_words

final_res = ""
emoji_count = 0
curr_words = 0
res_words = len(res.split())
gen = EmojiGenerator()

# Scales probability down as emoji frequency approaches average frequency
for word in res.split():
	final_res = final_res + word + ' '
	emoj = gen.get_emoji(word, probability_emoji)
	if emoj:
		final_res = final_res + emoj + ' '
		emoji_count = emoji_count + 1
	res_words = res_words + 1
	probability_emoji = 1.2 - 0.5 * emoji_count / avg_emojs - 0.5 * curr_words / res_words


file.write(final_res.strip())
file.close()

# Copy emoji.txt to clipboard
call(['bash', 'copy_emoji.sh'])